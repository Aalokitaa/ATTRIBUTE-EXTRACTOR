import os
import sys
# Add project root to path to resolve src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import pickle
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Import rule extractor and vocabulary details
from src.models.rule_based_extractor import RuleBasedExtractor
from src.vocabulary import FEATURE_MAP, VOCABULARY
from src.generate_data import main as generate_data

def load_dataset(file_path):
    dataset = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                dataset.append(json.loads(line.strip()))
    return dataset

def get_rule_features(text, rule_extractor):
    res = rule_extractor.extract(text)
    feats = []
    for attr, canonical in FEATURE_MAP:
        val = res[attr]
        if attr == "Color":
            matched = 1.0 if canonical in val else 0.0
        else:
            matched = 1.0 if val == canonical else 0.0
        feats.append(matched)
    return feats

def main():
    train_path = os.path.join("data", "train.jsonl")
    
    # Force re-generation of splits to ensure capitalized keys are used
    print("Re-generating dataset splits to apply capitalized keys...")
    generate_data()

    # Load train data
    train_data = load_dataset(train_path)
    print(f"Loaded {len(train_data)} training examples.")

    # Prepare inputs
    X_train_raw = [example["description"] for example in train_data]

    # Initialize TF-IDF Vectorizer
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_tfidf = vectorizer.fit_transform(X_train_raw).toarray()

    # Instantiate Rule-Based Extractor for match flag features
    rule_extractor = RuleBasedExtractor()
    X_rule = np.array([get_rule_features(x, rule_extractor) for x in X_train_raw])

    # Stack TF-IDF features and rule match flags horizontally
    X_train_combined = np.hstack([X_tfidf, X_rule])
    print(f"Feature matrix shape: {X_train_combined.shape}")

    classifiers = {}
    fallback_classes = {}
    
    # 1. Train classifiers for single-value fields
    single_val_attrs = ["Silhouette", "Fabric", "Neckline", "Sleeve", "Length", "Embellishment", "Category"]
    for attr in single_val_attrs:
        # Collect raw targets (None becomes "None")
        y_raw = [example[attr] if example[attr] is not None else "None" for example in train_data]
        
        # Count frequencies
        counts = Counter(y_raw)
        print(f"\nTarget class counts for '{attr}': {dict(counts)}")
        
        # Identify classes with fewer than 3 examples
        fallback = set()
        for label, count in counts.items():
            if label != "None" and count < 3:
                fallback.add(label)
                
        fallback_classes[attr] = fallback
        if fallback:
            print(f"  [Fallback classes identified: {fallback}]")
            
        # Map fallback classes to "None" in the ML target
        y_train = [val if val not in fallback else "None" for val in y_raw]
        unique_classes = set(y_train)
        
        # If we have less than 2 classes left (e.g. only "None"), we skip training entirely
        if len(unique_classes) < 2:
            print(f"  [Skipping training for '{attr}' - insufficient classes. Falling back entirely to rule-based.]")
            classifiers[attr] = None
        else:
            print(f"  [Training ML classifier for '{attr}' on classes: {unique_classes}]")
            clf = LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000)
            clf.fit(X_train_combined, y_train)
            classifiers[attr] = clf

    # 2. Train classifiers for multi-value field (Color)
    print("\nProcessing multi-value attribute 'Color'...")
    color_classifiers = {}
    fallback_colors = set()
    
    # Count frequency of each color in the training set
    color_counts = Counter()
    for example in train_data:
        for c in example["Color"]:
            color_counts[c] += 1
            
    print(f"Color counts in training set: {dict(color_counts)}")
    
    for color in VOCABULARY["Color"].keys():
        count = color_counts.get(color, 0)
        if count < 3:
            print(f"  Skipping training for color '{color}' (count={count}). Fallback to rule-based.")
            fallback_colors.add(color)
        else:
            print(f"  Training binary classifier for color '{color}' (count={count})...")
            # Binary labels: 1 if color is present, 0 otherwise
            y_bin = [1 if color in example["Color"] else 0 for example in train_data]
            
            clf = LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000)
            clf.fit(X_train_combined, y_bin)
            color_classifiers[color] = clf

    # Save model artifacts
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "attribute_extractor.pkl")
    print(f"\nSaving model artifacts to {model_path}...")
    
    model_data = {
        "vectorizer": vectorizer,
        "classifiers": classifiers,
        "fallback_classes": fallback_classes,
        "color_classifiers": color_classifiers,
        "fallback_colors": fallback_colors
    }
    
    with open(model_path, "wb") as f:
        pickle.dump(model_data, f)
        
    print("Model training completed successfully!")

if __name__ == "__main__":
    main()
