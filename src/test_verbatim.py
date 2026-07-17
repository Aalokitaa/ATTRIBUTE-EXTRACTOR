import os
import sys
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.rule_based_extractor import RuleBasedExtractor
from src.models.ml_extractor import MLExtractor

SEEDS = [
    "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue",
    "Sparkly sequin fitted prom gown featuring a deep illusion neckline and open back",
    "Off shoulder satin ball gown with corset bodice and sweep train in royal navy",
    "Lace mermaid wedding dress with long sleeves and scalloped hem",
    "Short cocktail dress with feather trim and beaded waist detail",
    "Tulle A line evening gown with floral embroidery and cap sleeves",
    "Stretch jersey sheath dress with ruched waist and side slit",
    "Strapless sweetheart neckline glitter gown with layered skirt",
    "One shoulder draped chiffon dress with high slit and empire waist",
    "Velvet winter formal dress with square neckline and puff sleeves"
]

def main():
    rule = RuleBasedExtractor()
    ml = MLExtractor()
    
    print("--- EVALUATING SEEDS WITH RULE-BASED ---")
    for idx, text in enumerate(SEEDS):
        res = rule.extract(text)
        # remove extra debug fields for minimal json output
        clean_res = {k: v for k, v in res.items() if k not in ["confidence", "matched_terms", "fallback_triggered"]}
        print(f"Seed {idx+1}: {text}")
        print(json.dumps(clean_res, indent=2))
        print()
        
    print("\n--- EVALUATING SEEDS WITH ML ---")
    for idx, text in enumerate(SEEDS):
        res = ml.extract(text)
        clean_res = {k: v for k, v in res.items() if k not in ["confidence", "matched_terms", "fallback_triggered"]}
        print(f"Seed {idx+1}: {text}")
        print(json.dumps(clean_res, indent=2))
        print()

if __name__ == "__main__":
    main()
