# Controlled Vocabulary for Product Attribute Extraction

VOCABULARY = {
    "Silhouette": {
        "A-line": ["a-line", "a line", "a-line silhouette"],
        "mermaid": ["mermaid", "mermaid silhouette", "trumpet", "trumpet silhouette"],
        "ball gown": ["ball gown", "ballgown", "princess skirt", "princess gown"],
        "sheath": ["sheath", "column", "column dress", "sheath silhouette"],
        "fit and flare": ["fit and flare", "fit & flare", "fit-and-flare", "fit n flare"]
    },
    "Fabric": {
        "chiffon": ["chiffon", "silk chiffon", "poly chiffon"],
        "satin": ["satin", "duchess satin", "silky satin"],
        "lace": ["lace", "chantilly lace", "guipure lace", "floral lace"],
        "tulle": ["tulle", "layered tulle", "soft tulle"],
        "velvet": ["velvet", "stretch velvet"],
        "sequin": ["sequin", "sequins", "sequined", "sparkly sequin", "glittering sequin"],
        "jersey": ["jersey", "stretch jersey", "matte jersey"]
    },
    "Neckline": {
        "V neck": ["v neck", "v-neck", "v neckline", "deep v", "deep v-neck"],
        "sweetheart": ["sweetheart", "sweetheart neckline", "sweetheart neck"],
        "off shoulder": ["off shoulder", "off-shoulder", "off the shoulder", "off-the-shoulder"],
        "square": ["square", "square neckline", "square neck"],
        "illusion": ["illusion", "illusion neckline", "sheer illusion"],
        "one shoulder": ["one shoulder", "one-shoulder", "single shoulder"]
    },
    "Sleeve": {
        "long sleeve": ["long sleeve", "long sleeves", "long-sleeved"],
        "cap sleeve": ["cap sleeve", "cap sleeves"],
        "puff sleeve": ["puff sleeve", "puff sleeves", "puffed sleeves"],
        "sleeveless": ["sleeveless", "sleeveless silhouette"],
        "strapless": ["strapless", "strapless bodice"]
    },
    "Length": {
        "floor length": ["floor length", "floor-length", "maxi", "full length", "full-length"],
        "short": ["short", "short length", "above the knee"],
        "mini": ["mini", "mini length", "thigh-length"],
        "sweep train": ["sweep train", "court train", "chapel train", "with train", "puddle train"],
        "high slit": ["high slit", "side slit", "thigh slit", "thigh-high slit", "leg slit"],
        "midi": ["midi", "midi length", "midi-length", "tea length", "tea-length"],
        "knee length": ["knee length", "knee-length", "to the knee"],
        "ankle length": ["ankle length", "ankle-length", "to the ankle"]
    },
    "Embellishment": {
        "beaded": ["beaded", "beading", "beadwork", "crystal beaded"],
        "sequin": ["sequin", "sequins", "sequined", "sparkly sequins"],
        "embroidery": ["embroidery", "embroidered", "floral embroidery", "appliqués", "applique"],
        "feather trim": ["feather trim", "feather-trimmed", "feathers"],
        "ruched": ["ruched", "ruching", "draped ruching"],
        "pleated": ["pleated", "pleats", "pleat", "pleated bodice"]
    },
    "Color": {
        "sage": ["sage", "sage green"],
        "dusty blue": ["dusty blue", "slate blue"],
        "royal navy": ["royal navy", "navy", "navy blue"],
        "emerald": ["emerald", "emerald green"],
        "black": ["black", "onyx"],
        "white": ["white", "bright white"],
        "ivory": ["ivory", "cream"],
        "red": ["red", "crimson", "scarlet"],
        "gold": ["gold", "metallic gold"],
        "silver": ["silver", "metallic silver"],
        "rose gold": ["rose gold"],
        "blush": ["blush", "blush pink"],
        "champagne": ["champagne"],
        "lavender": ["lavender", "lilac"],
        "burgundy": ["burgundy", "wine", "cabernet"],
        "plum": ["plum"],
        "purple": ["purple", "violet", "plum purple"],
        "pink": ["pink", "dusty pink", "fuchsia", "magenta"],
        "blue": ["blue", "baby blue", "royal blue", "light blue", "sky blue"],
        "green": ["green", "forest green", "olive green", "mint green", "hunter green"]
    },
    "Category": {
        "bridesmaid dress": ["bridesmaid dress", "bridesmaid gown", "bridesmaids dress"],
        "prom gown": ["prom gown", "prom dress"],
        "wedding dress": ["wedding dress", "wedding gown", "bridal gown", "bridal dress"],
        "cocktail dress": ["cocktail dress", "party dress", "semi-formal dress"],
        "evening gown": ["evening gown", "formal dress", "evening dress", "formal gown"]
    }
}

# Generate a list of (attribute, canonical_value) in a deterministic order
FEATURE_MAP = []
for attr in ["Silhouette", "Fabric", "Neckline", "Sleeve", "Length", "Embellishment", "Color", "Category"]:
    for canonical in VOCABULARY[attr].keys():
        FEATURE_MAP.append((attr, canonical))
