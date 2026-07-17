import os
import json
import random

DATASET = [
    # 1-10 Seed Examples
    {
        "description": "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue",
        "silhouette": None, "fabric": "chiffon", "neckline": "V neck", "sleeve": None, "length": "floor length", "embellishment": "pleated",
        "color": ["sage", "dusty blue"], "category": "bridesmaid dress"
    },
    {
        "description": "Sparkly sequin fitted prom gown featuring a deep illusion neckline and open back",
        "silhouette": None, "fabric": "sequin", "neckline": "illusion", "sleeve": None, "length": None, "embellishment": "sequin",
        "color": [], "category": "prom gown"
    },
    {
        "description": "Off shoulder satin ball gown with corset bodice and sweep train in royal navy",
        "silhouette": "ball gown", "fabric": "satin", "neckline": "off shoulder", "sleeve": None, "length": "sweep train", "embellishment": None,
        "color": ["royal navy"], "category": "evening gown"
    },
    {
        "description": "Lace mermaid wedding dress with long sleeves and scalloped hem",
        "silhouette": "mermaid", "fabric": "lace", "neckline": None, "sleeve": "long sleeve", "length": None, "embellishment": None,
        "color": [], "category": "wedding dress"
    },
    {
        "description": "Short cocktail dress with feather trim and beaded waist detail",
        "silhouette": None, "fabric": None, "neckline": None, "sleeve": None, "length": "short", "embellishment": "feather trim",
        "color": [], "category": "cocktail dress"
    },
    {
        "description": "Tulle A line evening gown with floral embroidery and cap sleeves",
        "silhouette": "A-line", "fabric": "tulle", "neckline": None, "sleeve": "cap sleeve", "length": None, "embellishment": "embroidery",
        "color": [], "category": "evening gown"
    },
    {
        "description": "Stretch jersey sheath dress with ruched waist and side slit",
        "silhouette": "sheath", "fabric": "jersey", "neckline": None, "sleeve": None, "length": "high slit", "embellishment": "ruched",
        "color": [], "category": None
    },
    {
        "description": "Strapless sweetheart neckline glitter gown with layered skirt",
        "silhouette": None, "fabric": None, "neckline": "sweetheart", "sleeve": "strapless", "length": None, "embellishment": None,
        "color": [], "category": None
    },
    {
        "description": "One shoulder draped chiffon dress with high slit and empire waist",
        "silhouette": None, "fabric": "chiffon", "neckline": "one shoulder", "sleeve": None, "length": "high slit", "embellishment": None,
        "color": [], "category": None
    },
    {
        "description": "Velvet winter formal dress with square neckline and puff sleeves",
        "silhouette": None, "fabric": "velvet", "neckline": "square", "sleeve": "puff sleeve", "length": None, "embellishment": None,
        "color": [], "category": "evening gown"
    },
    # 11-20
    {
        "description": "Emerald green A-line bridesmaid dress in soft chiffon with a pleated bodice and V-neck",
        "silhouette": "A-line", "fabric": "chiffon", "neckline": "V neck", "sleeve": None, "length": None, "embellishment": "pleated",
        "color": ["emerald"], "category": "bridesmaid dress"
    },
    {
        "description": "A romantic wedding gown in white floral lace with long sleeves and a long sweep train",
        "silhouette": None, "fabric": "lace", "neckline": None, "sleeve": "long sleeve", "length": "sweep train", "embellishment": None,
        "color": ["white"], "category": "wedding dress"
    },
    {
        "description": "Charming short cocktail dress featuring a sheer illusion neckline and delicate beading in champagne",
        "silhouette": None, "fabric": None, "neckline": "illusion", "sleeve": None, "length": "short", "embellishment": "beaded",
        "color": ["champagne"], "category": "cocktail dress"
    },
    {
        "description": "Sparkly gold sequin prom gown with a sweetheart neckline and strapless corset back",
        "silhouette": None, "fabric": "sequin", "neckline": "sweetheart", "sleeve": "strapless", "length": None, "embellishment": "sequin",
        "color": ["gold"], "category": "prom gown"
    },
    {
        "description": "Velvet evening gown in royal navy with a square neckline, puff sleeves, and a high slit",
        "silhouette": None, "fabric": "velvet", "neckline": "square", "sleeve": "puff sleeve", "length": "high slit", "embellishment": None,
        "color": ["royal navy"], "category": "evening gown"
    },
    {
        "description": "Simple stretch jersey sheath dress in classic black featuring a side slit and a sleeveless halter style",
        "silhouette": "sheath", "fabric": "jersey", "neckline": None, "sleeve": "sleeveless", "length": "high slit", "embellishment": None,
        "color": ["black"], "category": None
    },
    {
        "description": "Blush pink tulle A-line evening dress with floral embroidery and cap sleeves",
        "silhouette": "A-line", "fabric": "tulle", "neckline": None, "sleeve": "cap sleeve", "length": None, "embellishment": "embroidery",
        "color": ["blush"], "category": "evening gown"
    },
    {
        "description": "Gleaming silver satin ball gown with an off shoulder neckline and a dramatic sweep train",
        "silhouette": "ball gown", "fabric": "satin", "neckline": "off shoulder", "sleeve": None, "length": "sweep train", "embellishment": None,
        "color": ["silver"], "category": "evening gown"
    },
    {
        "description": "Mini length party dress with a one shoulder draped bodice in lavender chiffon",
        "silhouette": None, "fabric": "chiffon", "neckline": "one shoulder", "sleeve": None, "length": "mini", "embellishment": None,
        "color": ["lavender"], "category": "cocktail dress"
    },
    {
        "description": "Elegant wine burgundy bridesmaids dress with a V-neckline and pleated satin skirt",
        "silhouette": None, "fabric": "satin", "neckline": "V neck", "sleeve": None, "length": None, "embellishment": "pleated",
        "color": ["burgundy"], "category": "bridesmaid dress"
    },
    # 21-30
    {
        "description": "Dazzling sequined mermaid wedding dress with a deep sweetheart neckline and strapless style in ivory",
        "silhouette": "mermaid", "fabric": "sequin", "neckline": "sweetheart", "sleeve": "strapless", "length": None, "embellishment": "sequin",
        "color": ["ivory"], "category": "wedding dress"
    },
    {
        "description": "A floor length stretch jersey sheath evening gown with a high slit and long sleeves in crimson red",
        "silhouette": "sheath", "fabric": "jersey", "neckline": None, "sleeve": "long sleeve", "length": "floor length", "embellishment": None,
        "color": ["red"], "category": "evening gown"
    },
    {
        "description": "A-line wedding gown with floral embroidery on the bodice, a sheer illusion neckline, and cap sleeves in bright white",
        "silhouette": "A-line", "fabric": None, "neckline": "illusion", "sleeve": "cap sleeve", "length": None, "embellishment": "embroidery",
        "color": ["white"], "category": "wedding dress"
    },
    {
        "description": "Plum purple winter formal gown in soft velvet with a square neckline and long sleeves",
        "silhouette": None, "fabric": "velvet", "neckline": "square", "sleeve": "long sleeve", "length": None, "embellishment": None,
        "color": ["plum"], "category": "evening gown"
    },
    {
        "description": "Sleeveless sage green chiffon bridesmaid dress featuring a ruched waist and a sweetheart neckline",
        "silhouette": None, "fabric": "chiffon", "neckline": "sweetheart", "sleeve": "sleeveless", "length": None, "embellishment": "ruched",
        "color": ["sage"], "category": "bridesmaid dress"
    },
    {
        "description": "Short cocktail dress in glittering rose gold sequins with a high neckline and sleeveless design",
        "silhouette": None, "fabric": "sequin", "neckline": None, "sleeve": "sleeveless", "length": "short", "embellishment": "sequin",
        "color": ["rose gold"], "category": "cocktail dress"
    },
    {
        "description": "Luxurious royal navy satin ball gown with an off shoulder neck and sweep train",
        "silhouette": "ball gown", "fabric": "satin", "neckline": "off shoulder", "sleeve": None, "length": "sweep train", "embellishment": None,
        "color": ["royal navy"], "category": "evening gown"
    },
    {
        "description": "Off-the-shoulder mermaid prom dress in red crepe with a dramatic thigh-high slit",
        "silhouette": "mermaid", "fabric": None, "neckline": "off shoulder", "sleeve": None, "length": "high slit", "embellishment": None,
        "color": ["red"], "category": "prom gown"
    },
    {
        "description": "One shoulder floor length evening gown in pleated dusty blue chiffon with a side slit",
        "silhouette": None, "fabric": "chiffon", "neckline": "one shoulder", "sleeve": None, "length": "floor length", "embellishment": "pleated",
        "color": ["dusty blue"], "category": "evening gown"
    },
    {
        "description": "Strapless ball gown wedding dress in layered tulle with crystal beaded bodice in ivory",
        "silhouette": "ball gown", "fabric": "tulle", "neckline": None, "sleeve": "strapless", "length": None, "embellishment": "beaded",
        "color": ["ivory"], "category": "wedding dress"
    },
    # 31-40
    {
        "description": "Sheath cocktail dress in black stretch jersey featuring a deep V-neck and cap sleeves",
        "silhouette": "sheath", "fabric": "jersey", "neckline": "V neck", "sleeve": "cap sleeve", "length": None, "embellishment": None,
        "color": ["black"], "category": "cocktail dress"
    },
    {
        "description": "Gorgeous fit and flare prom dress in sequined lace with a sweetheart neckline and sweep train",
        "silhouette": "fit and flare", "fabric": "lace", "neckline": "sweetheart", "sleeve": None, "length": "sweep train", "embellishment": "sequin",
        "color": [], "category": "prom gown"
    },
    {
        "description": "Boho wedding gown with long puff sleeves and floral embroidery in soft ivory tulle",
        "silhouette": None, "fabric": "tulle", "neckline": None, "sleeve": "puff sleeve", "length": None, "embellishment": "embroidery",
        "color": ["ivory"], "category": "wedding dress"
    },
    {
        "description": "Chic mini length party dress featuring feather trim and a square neckline in bright white satin",
        "silhouette": None, "fabric": "satin", "neckline": "square", "sleeve": None, "length": "mini", "embellishment": "feather trim",
        "color": ["white"], "category": "cocktail dress"
    },
    {
        "description": "Sage green chiffon bridesmaid dress with a one shoulder strap, ruched bodice, and floor length skirt",
        "silhouette": None, "fabric": "chiffon", "neckline": "one shoulder", "sleeve": None, "length": "floor length", "embellishment": "ruched",
        "color": ["sage"], "category": "bridesmaid dress"
    },
    {
        "description": "Stunning black velvet mermaid formal gown with a sweetheart neckline and long sleeves",
        "silhouette": "mermaid", "fabric": "velvet", "neckline": "sweetheart", "sleeve": "long sleeve", "length": None, "embellishment": None,
        "color": ["black"], "category": "evening gown"
    },
    {
        "description": "Glittering silver fit and flare evening gown with an illusion neckline and sleeveless bodice",
        "silhouette": "fit and flare", "fabric": None, "neckline": "illusion", "sleeve": "sleeveless", "length": None, "embellishment": None,
        "color": ["silver"], "category": "evening gown"
    },
    {
        "description": "A short A-line bridesmaid dress in lavender chiffon with a pleated bodice and V neck",
        "silhouette": "A-line", "fabric": "chiffon", "neckline": "V neck", "sleeve": None, "length": "short", "embellishment": "pleated",
        "color": ["lavender"], "category": "bridesmaid dress"
    },
    {
        "description": "Crimson red off shoulder satin ball gown featuring a fitted corset bodice and sweep train",
        "silhouette": "ball gown", "fabric": "satin", "neckline": "off shoulder", "sleeve": None, "length": "sweep train", "embellishment": None,
        "color": ["red"], "category": "evening gown"
    },
    {
        "description": "Elegant ivory chantilly lace wedding gown with cap sleeves and a long sweep train",
        "silhouette": None, "fabric": "lace", "neckline": None, "sleeve": "cap sleeve", "length": "sweep train", "embellishment": None,
        "color": ["ivory"], "category": "wedding dress"
    },
    # 41-50
    {
        "description": "Semi-formal party dress in sparkly rose gold sequins with puff sleeves and short hemline",
        "silhouette": None, "fabric": "sequin", "neckline": None, "sleeve": "puff sleeve", "length": "short", "embellishment": "sequin",
        "color": ["rose gold"], "category": "cocktail dress"
    },
    {
        "description": "A-line evening gown in navy blue tulle with floral embroidery and off the shoulder neckline",
        "silhouette": "A-line", "fabric": "tulle", "neckline": "off shoulder", "sleeve": None, "length": None, "embellishment": "embroidery",
        "color": ["royal navy"], "category": "evening gown"
    },
    {
        "description": "Stretch jersey sheath evening dress with a deep V neckline and high slit in classic black",
        "silhouette": "sheath", "fabric": "jersey", "neckline": "V neck", "sleeve": None, "length": "high slit", "embellishment": None,
        "color": ["black"], "category": "evening gown"
    },
    {
        "description": "Strapless sweetheart neckline wedding dress in white satin with a layered sweep train",
        "silhouette": None, "fabric": "satin", "neckline": "sweetheart", "sleeve": "strapless", "length": "sweep train", "embellishment": None,
        "color": ["white"], "category": "wedding dress"
    },
    {
        "description": "One shoulder draped chiffon bridesmaid gown in dusty blue with a side leg slit",
        "silhouette": None, "fabric": "chiffon", "neckline": "one shoulder", "sleeve": None, "length": "high slit", "embellishment": None,
        "color": ["dusty blue"], "category": "bridesmaid dress"
    },
    {
        "description": "Puff sleeve velvet winter formal dress with a square neck in deep emerald green",
        "silhouette": None, "fabric": "velvet", "neckline": "square", "sleeve": "puff sleeve", "length": None, "embellishment": None,
        "color": ["emerald"], "category": "evening gown"
    },
    {
        "description": "Stunning fit and flare evening gown in champagne lace featuring long sleeves and a V-neckline",
        "silhouette": "fit and flare", "fabric": "lace", "neckline": "V neck", "sleeve": "long sleeve", "length": None, "embellishment": None,
        "color": ["champagne"], "category": "evening gown"
    },
    {
        "description": "A short cocktail dress in pink crepe with feather trim and off-shoulder sleeves",
        "silhouette": None, "fabric": None, "neckline": "off shoulder", "sleeve": None, "length": "short", "embellishment": "feather trim",
        "color": [], "category": "cocktail dress"
    },
    {
        "description": "Lilac lavender tulle A-line evening dress with floral embroidery and strapless bodice",
        "silhouette": "A-line", "fabric": "tulle", "neckline": None, "sleeve": "strapless", "length": None, "embellishment": "embroidery",
        "color": ["lavender"], "category": "evening gown"
    },
    {
        "description": "Glamorous silver sequined mermaid gown featuring a deep V-neck and sweep train",
        "silhouette": "mermaid", "fabric": "sequin", "neckline": "V neck", "sleeve": None, "length": "sweep train", "embellishment": "sequin",
        "color": ["silver"], "category": "evening gown"
    },
    # 51-60
    {
        "description": "Sleeveless bridesmaid dress in sage green pleated chiffon with a sweetheart neckline",
        "silhouette": None, "fabric": "chiffon", "neckline": "sweetheart", "sleeve": "sleeveless", "length": None, "embellishment": "pleated",
        "color": ["sage"], "category": "bridesmaid dress"
    },
    {
        "description": "Stunning ivory lace wedding dress with a sheer illusion neckline and long sleeves",
        "silhouette": None, "fabric": "lace", "neckline": "illusion", "sleeve": "long sleeve", "length": None, "embellishment": None,
        "color": ["ivory"], "category": "wedding dress"
    },
    {
        "description": "Cocktail dress in red stretch jersey featuring a ruched waist and mini length",
        "silhouette": None, "fabric": "jersey", "neckline": None, "sleeve": None, "length": "mini", "embellishment": "ruched",
        "color": ["red"], "category": "cocktail dress"
    },
    {
        "description": "Strapless sweetheart neckline evening gown in gold satin with a high slit",
        "silhouette": None, "fabric": "satin", "neckline": "sweetheart", "sleeve": "strapless", "length": "high slit", "embellishment": None,
        "color": ["gold"], "category": "evening gown"
    },
    {
        "description": "One shoulder bridesmaid gown in dusty blue chiffon with a pleated bodice and floor length skirt",
        "silhouette": None, "fabric": "chiffon", "neckline": "one shoulder", "sleeve": None, "length": "floor length", "embellishment": "pleated",
        "color": ["dusty blue"], "category": "bridesmaid dress"
    },
    {
        "description": "Emerald green velvet winter formal dress with puff sleeves and square neckline",
        "silhouette": None, "fabric": "velvet", "neckline": "square", "sleeve": "puff sleeve", "length": None, "embellishment": None,
        "color": ["emerald"], "category": "evening gown"
    },
    {
        "description": "Sparkly sequin prom gown featuring an illusion neckline and sweep train in royal navy and silver",
        "silhouette": None, "fabric": "sequin", "neckline": "illusion", "sleeve": None, "length": "sweep train", "embellishment": "sequin",
        "color": ["royal navy", "silver"], "category": "prom gown"
    },
    {
        "description": "Lace mermaid wedding dress in white with cap sleeves and a long sweep train",
        "silhouette": "mermaid", "fabric": "lace", "neckline": None, "sleeve": "cap sleeve", "length": "sweep train", "embellishment": None,
        "color": ["white"], "category": "wedding dress"
    },
    {
        "description": "Short cocktail dress with a square neck and feather trim in black satin",
        "silhouette": None, "fabric": "satin", "neckline": "square", "sleeve": None, "length": "short", "embellishment": "feather trim",
        "color": ["black"], "category": "cocktail dress"
    },
    {
        "description": "Tulle A-line evening gown featuring floral embroidery, sleeveless bodice, and floor length skirt in blush",
        "silhouette": "A-line", "fabric": "tulle", "neckline": None, "sleeve": "sleeveless", "length": "floor length", "embellishment": "embroidery",
        "color": ["blush"], "category": "evening gown"
    }
]

def main():
    os.makedirs("data", exist_ok=True)
    
    # Capitalize the keys dynamically
    capitalized_dataset = []
    for item in DATASET:
        new_item = {}
        for k, v in item.items():
            if k == "description":
                new_item[k] = v
            else:
                new_item[k.capitalize()] = v
        capitalized_dataset.append(new_item)
    
    # Write labeled_dataset.jsonl
    labeled_path = os.path.join("data", "labeled_dataset.jsonl")
    with open(labeled_path, "w", encoding="utf-8") as f:
        for item in capitalized_dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Wrote {len(capitalized_dataset)} items to {labeled_path}")

    # Set seed for reproducibility
    random.seed(42)
    shuffled = list(capitalized_dataset)
    random.shuffle(shuffled)

    # 80/20 split
    n = len(shuffled)
    n_train = int(n * 0.80)
    
    train_set = shuffled[:n_train]
    test_set = shuffled[n_train:]

    for name, subset in [("train.jsonl", train_set), ("test.jsonl", test_set)]:
        path = os.path.join("data", name)
        with open(path, "w", encoding="utf-8") as f:
            for item in subset:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"Wrote {len(subset)} items to {path}")

if __name__ == "__main__":
    main()
