import re
from src.models.base import BaseExtractor
from src.vocabulary import VOCABULARY

class RuleBasedExtractor(BaseExtractor):
    def __init__(self):
        # Precompile regular expressions for all synonyms to optimize search speed
        self.rules = {}
        for attribute, value_map in VOCABULARY.items():
            self.rules[attribute] = []
            for canonical, synonyms in value_map.items():
                for synonym in synonyms:
                    # Use word boundaries to avoid substring matching (e.g. "lace" inside "place")
                    pattern = re.compile(r'\b' + re.escape(synonym) + r'\b', re.IGNORECASE)
                    self.rules[attribute].append({
                        "canonical": canonical,
                        "synonym": synonym,
                        "pattern": pattern
                    })

    def extract(self, text: str) -> dict:
        if not text:
            return {
                "Silhouette": None, "Fabric": None, "Neckline": None, "Sleeve": None,
                "Length": None, "Embellishment": None, "Color": [], "Category": None,
                "confidence": {}, "matched_terms": {}
            }

        extracted = {}
        confidence = {}
        matched_terms = {}

        for attribute in VOCABULARY.keys():
            matches = []
            for rule in self.rules[attribute]:
                for match in rule["pattern"].finditer(text):
                    matches.append({
                        "canonical": rule["canonical"],
                        "matched_text": match.group(0),
                        "start": match.start()
                    })

            # Sort matches by their appearance in the text
            matches.sort(key=lambda x: x["start"])

            if attribute == "Color":
                # For color, return all unique matching canonical colors
                colors = []
                seen = set()
                matched_words = []
                for m in matches:
                    if m["canonical"] not in seen:
                        seen.add(m["canonical"])
                        colors.append(m["canonical"])
                        matched_words.append(m["matched_text"])
                extracted[attribute] = colors
                confidence[attribute] = 1.0 if colors else 0.0
                matched_terms[attribute] = matched_words
            else:
                # For single-value fields, take the first occurrence in the text
                if matches:
                    extracted[attribute] = matches[0]["canonical"]
                    confidence[attribute] = 1.0
                    matched_terms[attribute] = [matches[0]["matched_text"]]
                else:
                    extracted[attribute] = None
                    confidence[attribute] = 0.0
                    matched_terms[attribute] = []

        return {
            **extracted,
            "confidence": confidence,
            "matched_terms": matched_terms
        }
