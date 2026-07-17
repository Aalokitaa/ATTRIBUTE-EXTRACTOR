# Product Attribute Extraction Pipeline

This repository implements a complete, demo-ready AI/NLP pipeline that extracts structured apparel attributes from unstructured fashion product descriptions.

## Problem Definition
Given free-text fashion descriptions, the pipeline extracts a structured JSON object containing 8 attribute fields:
- `silhouette` (canonical values e.g., A-line, mermaid, ball gown, sheath, fit and flare)
- `fabric` (canonical values e.g., chiffon, satin, lace, tulle, velvet, sequin, jersey)
- `neckline` (canonical values e.g., V neck, sweetheart, off shoulder, square, illusion, one shoulder)
- `sleeve` (canonical values e.g., long sleeve, cap sleeve, puff sleeve, sleeveless, strapless)
- `length` (canonical values e.g., floor length, short, mini, sweep train, high slit)
- `embellishment` (canonical values e.g., beaded, sequin, embroidery, feather trim, ruched, pleated)
- `color` (list of colors e.g. ["sage", "dusty blue"])
- `category` (canonical values e.g., bridesmaid dress, prom gown, wedding dress, cocktail dress, evening gown)

---

## Design & Hybrid Approach

With a tiny labeled dataset (~60 rows), a pure ML classifier trained on raw TF-IDF suffers from sparsity and overfitting. Similarly, a pure LLM approach is expensive and requires API keys and network calls.

This project employs a **Hybrid Extractor**:
1. **Rule-Based Engine**: Matches synonyms against a central controlled vocabulary (`src/vocabulary.py`) using regular expressions with strict word boundaries (`\b(synonym)\b`).
2. **ML Classifier**: A Logistic Regression classifier that uses **stacked features** (TF-IDF + Rule-Based Match Flags). This provides statistical learning while incorporating high-precision rule indicators.
3. **Class-Level Fallback**: If a target label has `< 3` training examples in the training set (e.g. rare embellishments or colors), we skip training the ML model for that specific label and automatically fall back to the rule-based prediction for it, logging the fallback.

---

## Repository Structure

```
product-attribute-extraction/
├── README.md                # Top-level documentation
├── EVALUATION.md            # Detailed accuracy reporting
├── DEMO_SCRIPT.md           # Step-by-step commands and talking points
├── requirements.txt         # Pinned python dependencies
├── Dockerfile               # Container build configuration
├── data/
│   ├── README.md            # Labeled dataset details & ontology
│   ├── labeled_dataset.jsonl# Full 60-row curated dataset
│   ├── train.jsonl          # 80% Train split
│   └── test.jsonl           # 20% Test split
├── models/
│   └── attribute_extractor.pkl # Saved trained model artifacts
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py          # Extractor interface
│   │   ├── rule_based_extractor.py
│   │   └── ml_extractor.py  # Hybrid feature & fallback model
│   ├── __init__.py
│   ├── generate_data.py     # Seeds & splits the dataset
│   ├── train.py             # Model training script
│   ├── evaluate.py          # Evaluates performance on test set
│   └── vocabulary.py        # Controlled vocabulary mapping
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI service endpoints
│   └── schemas.py           # Pydantic schemas
└── tests/
    └── test_api.py          # pytest endpoint unit tests
```

---

## Setup and Run Instructions

### Prerequisites
- Python 3.10+
- (Optional) Docker

### 1. Local Setup
Clone this repository and install dependencies in your environment:
```bash
pip install -r "requirements.txt"
```

### 2. Generate Data & Train Model
To create the 80/20 train/test split and train the ML classifiers:
```bash
python "src/train.py"
```

### 3. Run Evaluation
To verify model accuracy and generate the comparative report:
```bash
python "src/evaluate.py"
```
Evaluation metrics are saved to [EVALUATION.md](EVALUATION.md) and compared side-by-side.

### 4. Run API locally
To launch the FastAPI development server:
```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive API docs will render at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Docker Support

To package and run the service inside a Docker container:

```bash
# Build the container
docker build -t "attribute-extractor:latest" .

# Run the container
docker run -p 8000:8000 "attribute-extractor:latest"
```
The endpoint is reachable at `http://localhost:8000/extract`.

---

## Verbatim Extraction Examples

Below are the exact request and response pairs for the 10 seed sentences run through the `POST /extract` API using the default `ml` strategy:

### Example 1

**Request Description:**
> "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue"}'
```

**API Response:**
```json
{
  "Silhouette": null,
  "Fabric": "chiffon",
  "Neckline": "V neck",
  "Sleeve": null,
  "Length": "floor length",
  "Embellishment": "pleated",
  "Color": [
    "sage",
    "dusty blue"
  ],
  "Category": "bridesmaid dress",
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.0,
    "Fabric": 0.9047071010357424,
    "Neckline": 0.7098289017030592,
    "Sleeve": 0.0,
    "Length": 0.8340568900485383,
    "Embellishment": 0.905856839486976,
    "Color": 0.9159746296693836,
    "Category": 0.9406844007061602
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 2

**Request Description:**
> "Sparkly sequin fitted prom gown featuring a deep illusion neckline and open back"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Sparkly sequin fitted prom gown featuring a deep illusion neckline and open back"}'
```

**API Response:**
```json
{
  "Silhouette": null,
  "Fabric": "sequin",
  "Neckline": "illusion",
  "Sleeve": null,
  "Length": null,
  "Embellishment": "sequin",
  "Color": [],
  "Category": "prom gown",
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.0,
    "Fabric": 0.3975327465783013,
    "Neckline": 0.3225007320254948,
    "Sleeve": 0.0,
    "Length": 0.0,
    "Embellishment": 0.691312590147468,
    "Color": 1.0,
    "Category": 0.6561140905749473
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 3

**Request Description:**
> "Off shoulder satin ball gown with corset bodice and sweep train in royal navy"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Off shoulder satin ball gown with corset bodice and sweep train in royal navy"}'
```

**API Response:**
```json
{
  "Silhouette": "ball gown",
  "Fabric": "satin",
  "Neckline": "off shoulder",
  "Sleeve": null,
  "Length": "sweep train",
  "Embellishment": null,
  "Color": [
    "royal navy"
  ],
  "Category": null,
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.8984651618418478,
    "Fabric": 0.8407957894015384,
    "Neckline": 0.8877910387642637,
    "Sleeve": 0.0,
    "Length": 0.8711213155201769,
    "Embellishment": 0.0,
    "Color": 0.9389012963210763,
    "Category": 0.0
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 4

**Request Description:**
> "Lace mermaid wedding dress with long sleeves and scalloped hem"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Lace mermaid wedding dress with long sleeves and scalloped hem"}'
```

**API Response:**
```json
{
  "Silhouette": "mermaid",
  "Fabric": "lace",
  "Neckline": null,
  "Sleeve": "long sleeve",
  "Length": null,
  "Embellishment": null,
  "Color": [],
  "Category": "wedding dress",
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.8213800675611717,
    "Fabric": 0.7249644015342711,
    "Neckline": 0.0,
    "Sleeve": 0.8181483513979343,
    "Length": 0.0,
    "Embellishment": 0.0,
    "Color": 1.0,
    "Category": 0.8499341886499223
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 5

**Request Description:**
> "Short cocktail dress with feather trim and beaded waist detail"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Short cocktail dress with feather trim and beaded waist detail"}'
```

**API Response:**
```json
{
  "Silhouette": null,
  "Fabric": null,
  "Neckline": null,
  "Sleeve": null,
  "Length": "short",
  "Embellishment": "feather trim",
  "Color": [],
  "Category": "cocktail dress",
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.0,
    "Fabric": 0.0,
    "Neckline": 0.0,
    "Sleeve": 0.0,
    "Length": 0.8196712110735843,
    "Embellishment": 0.8058918624163574,
    "Color": 1.0,
    "Category": 0.8766707228591807
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 6

**Request Description:**
> "Tulle A line evening gown with floral embroidery and cap sleeves"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Tulle A line evening gown with floral embroidery and cap sleeves"}'
```

**API Response:**
```json
{
  "Silhouette": "A-line",
  "Fabric": "tulle",
  "Neckline": null,
  "Sleeve": "cap sleeve",
  "Length": null,
  "Embellishment": "embroidery",
  "Color": [],
  "Category": "evening gown",
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.8883800289145216,
    "Fabric": 0.8104523182449542,
    "Neckline": 0.0,
    "Sleeve": 0.7763061615129679,
    "Length": 0.0,
    "Embellishment": 0.9107930355553752,
    "Color": 1.0,
    "Category": 0.8289008648795134
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 7

**Request Description:**
> "Stretch jersey sheath dress with ruched waist and side slit"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Stretch jersey sheath dress with ruched waist and side slit"}'
```

**API Response:**
```json
{
  "Silhouette": "sheath",
  "Fabric": "jersey",
  "Neckline": null,
  "Sleeve": null,
  "Length": "high slit",
  "Embellishment": null,
  "Color": [],
  "Category": null,
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.5178500800884419,
    "Fabric": 0.6827841899747547,
    "Neckline": 0.0,
    "Sleeve": 0.0,
    "Length": 0.5845025670709172,
    "Embellishment": 0.45804034600311677,
    "Color": 1.0,
    "Category": 0.0
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 8

**Request Description:**
> "Strapless sweetheart neckline glitter gown with layered skirt"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Strapless sweetheart neckline glitter gown with layered skirt"}'
```

**API Response:**
```json
{
  "Silhouette": null,
  "Fabric": null,
  "Neckline": "sweetheart",
  "Sleeve": "strapless",
  "Length": null,
  "Embellishment": null,
  "Color": [],
  "Category": null,
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.0,
    "Fabric": 0.0,
    "Neckline": 0.6371457425078711,
    "Sleeve": 0.6117377596076113,
    "Length": 0.0,
    "Embellishment": 0.0,
    "Color": 1.0,
    "Category": 0.0
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 9

**Request Description:**
> "One shoulder draped chiffon dress with high slit and empire waist"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "One shoulder draped chiffon dress with high slit and empire waist"}'
```

**API Response:**
```json
{
  "Silhouette": null,
  "Fabric": "chiffon",
  "Neckline": "one shoulder",
  "Sleeve": null,
  "Length": "high slit",
  "Embellishment": null,
  "Color": [],
  "Category": null,
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.0,
    "Fabric": 0.5151916700207718,
    "Neckline": 0.6447434249159417,
    "Sleeve": 0.0,
    "Length": 0.663016969447428,
    "Embellishment": 0.0,
    "Color": 1.0,
    "Category": 0.0
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

### Example 10

**Request Description:**
> "Velvet winter formal dress with square neckline and puff sleeves"

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{"description": "Velvet winter formal dress with square neckline and puff sleeves"}'
```

**API Response:**
```json
{
  "Silhouette": null,
  "Fabric": "velvet",
  "Neckline": "square",
  "Sleeve": "puff sleeve",
  "Length": null,
  "Embellishment": null,
  "Color": [],
  "Category": "evening gown",
  "strategy_used": "ml",
  "confidence": {
    "Silhouette": 0.0,
    "Fabric": 0.8262756360672655,
    "Neckline": 0.8338672059790954,
    "Sleeve": 0.8353144848043164,
    "Length": 0.0,
    "Embellishment": 0.0,
    "Color": 1.0,
    "Category": 0.8648414097304833
  },
  "matched_terms": {
    "Silhouette": [],
    "Fabric": [],
    "Neckline": [],
    "Sleeve": [],
    "Length": [],
    "Embellishment": [],
    "Color": [],
    "Category": []
  }
}
```

---

## Known Limitations and Next Steps
1. **Out of Vocabulary (OOV) Terms**: The rule-based engine and the stacked binary features only capture matches in our controlled vocabulary list. Adding word vector embeddings (like GloVe or BERT) will help generalise matching to synonyms not in the seed vocabulary.
2. **Context Blindness in Rules**: A simple keyword-matching approach might mismatch negation (e.g. "does not have long sleeves" still matches "long sleeve"). Transitioning to a proper NER parser (like spaCy Custom NER) will resolve context.
3. **Small Test Set**: The 12-sample test set makes performance metrics highly sensitive. We suggest scaling the dataset using automated synthesizers to at least 500 records before launching to production.
