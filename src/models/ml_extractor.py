import os
import pickle
import numpy as np
from src.models.base import BaseExtractor
from src.models.rule_based_extractor import RuleBasedExtractor
from src.vocabulary import FEATURE_MAP, VOCABULARY

class MLExtractor(BaseExtractor):
    def __init__(self, model_path="models/attribute_extractor.pkl"):
        self.model_path = model_path
        self.loaded = False
        
        # Instantiate rule extractor for feature engineering and fallbacks
        self.rule_extractor = RuleBasedExtractor()
        
        self.vectorizer = None
        self.classifiers = {}
        self.fallback_classes = {}
        self.color_classifiers = {}
        self.fallback_colors = set()
        
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            print(f"Warning: Model file not found at {self.model_path}. Please run src/train.py first.")

    def load_model(self):
        with open(self.model_path, "rb") as f:
            data = pickle.load(f)
        self.vectorizer = data["vectorizer"]
        self.classifiers = data["classifiers"]
        self.fallback_classes = data["fallback_classes"]
        self.color_classifiers = data["color_classifiers"]
        self.fallback_colors = data["fallback_colors"]
        self.loaded = True

    def _get_combined_features(self, text: str):
        # 1. TF-IDF features
        tfidf_feats = self.vectorizer.transform([text]).toarray()
        
        # 2. Rule match features (binary flags for all 55 canonical values)
        rule_res = self.rule_extractor.extract(text)
        binary_feats = []
        for attr, canonical in FEATURE_MAP:
            val = rule_res[attr]
            if attr == "Color":
                matched = 1.0 if canonical in val else 0.0
            else:
                matched = 1.0 if val == canonical else 0.0
            binary_feats.append(matched)
            
        binary_feats = np.array([binary_feats])
        
        # Stack TF-IDF and binary features horizontally
        return np.hstack([tfidf_feats, binary_feats])

    def extract(self, text: str) -> dict:
        if not self.loaded:
            # Fallback to rule-based entirely if ML model isn't trained yet
            return self.rule_extractor.extract(text)

        if not text:
            return {
                "Silhouette": None, "Fabric": None, "Neckline": None, "Sleeve": None,
                "Length": None, "Embellishment": None, "Color": [], "Category": None,
                "confidence": {k: 0.0 for k in ["Silhouette", "Fabric", "Neckline", "Sleeve", "Length", "Embellishment", "Color", "Category"]},
                "matched_terms": {k: [] for k in ["Silhouette", "Fabric", "Neckline", "Sleeve", "Length", "Embellishment", "Color", "Category"]},
                "fallback_triggered": {}
            }

        # Precompute rule-based prediction for gating and features
        rule_pred = self.rule_extractor.extract(text)
        features = self._get_combined_features(text)

        extracted = {}
        confidence = {}
        fallback_triggered = {}

        # 1. Single-value fields prediction with gating & fallback
        for attr in ["Silhouette", "Fabric", "Neckline", "Sleeve", "Length", "Embellishment", "Category"]:
            rule_val = rule_pred[attr]
            
            # GATING: If the rule-based extractor finds no occurrence of this attribute in the description,
            # we keep it as None to prevent machine learning hallucinations.
            if rule_val is None:
                extracted[attr] = None
                confidence[attr] = 0.0
                fallback_triggered[attr] = None
                continue
            
            # If there is a match, check if it's a fallback class
            is_fallback = rule_val in self.fallback_classes[attr]
            clf = self.classifiers.get(attr)
            
            if is_fallback or clf is None:
                extracted[attr] = rule_val
                confidence[attr] = 1.0  # Rule-based fallback has full confidence
                fallback_triggered[attr] = f"Class '{rule_val}' has < 3 training examples. Fell back to rule-based." if is_fallback else "Entire field skipped training. Fell back to rule-based."
            else:
                pred = clf.predict(features)[0]
                
                # Retrieve probability for prediction confidence
                if hasattr(clf, "predict_proba"):
                    probs = clf.predict_proba(features)[0]
                    classes = list(clf.classes_)
                    idx = classes.index(pred)
                    conf = float(probs[idx])
                else:
                    conf = 1.0

                if pred == "None":
                    # If ML predicts "None" but a rule match exists, we can trust the rule or return None.
                    # Since rule is high-precision, returning None here is conservative.
                    extracted[attr] = None
                else:
                    extracted[attr] = pred
                confidence[attr] = conf
                fallback_triggered[attr] = None

        # 2. Multi-value field (Color) prediction with gating & fallback
        pred_colors = []
        color_confidences = []
        fallback_triggered["Color"] = None
        triggered_colors = []

        # GATING: We only evaluate colors that were actually matched in the text by the rule-based engine.
        for color in rule_pred["Color"]:
            if color in self.fallback_colors:
                pred_colors.append(color)
                color_confidences.append(1.0)
                triggered_colors.append(color)
            else:
                clf = self.color_classifiers.get(color)
                if clf:
                    prob = clf.predict_proba(features)[0][1]
                    pred_colors.append(color)
                    color_confidences.append(float(prob))
                        
        if triggered_colors:
            fallback_triggered["Color"] = f"Colors {triggered_colors} have < 3 training examples. Fell back to rule-based."

        extracted["Color"] = pred_colors
        confidence["Color"] = sum(color_confidences) / len(color_confidences) if color_confidences else 0.0

        # Populate matched_terms based on successfully extracted values
        matched_terms = {}
        for attr in ["Silhouette", "Fabric", "Neckline", "Sleeve", "Length", "Embellishment", "Category"]:
            if extracted[attr] is not None:
                matched_terms[attr] = rule_pred["matched_terms"].get(attr, [])
            else:
                matched_terms[attr] = []
        
        if extracted["Color"]:
            matched_terms["Color"] = rule_pred["matched_terms"].get("Color", [])
        else:
            matched_terms["Color"] = []

        return {
            **extracted,
            "confidence": confidence,
            "matched_terms": matched_terms,
            "fallback_triggered": fallback_triggered
        }
