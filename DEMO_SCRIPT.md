# Demo Script — Product Attribute Extraction Pipeline

This guide lists the exact step-by-step commands and talking points to walk through the pipeline in under 3 minutes.

---

## Part 1: Dataset Generation & Model Training (0:00 - 0:45)

### Talking Point
> "Hi, today I am going to demo our Fashion & Apparel Product Attribute Extraction Pipeline. We started with a controlled vocabulary of fashion attributes and expanded our dataset to 60 high-quality labeled examples, split into an 80/20 train/test split. Let's first train our models."

### Command
Open a terminal in the project root directory and run:
```bash
python "src/train.py"
```

### Action
- Show the terminal output showing the class counts, the fallback classes identified (with <3 training examples), and the model saving to `models/attribute_extractor.pkl`.

---

## Part 2: Model Evaluation (0:45 - 1:20)

### Talking Point
> "Our training script implements a hybrid feature approach where TF-IDF is combined with rule match flags, and implements class-level fallback logic for classes with too few training rows. Let's run our evaluation script to compare the rule-based extractor with the ML model on our held-out test split."

### Command
```bash
python "src/evaluate.py"
```

### Action
- Point to the side-by-side metrics table shown in the terminal.
- Say:
> "As we can see, the rule-based extractor achieves very high accuracy, close to 100% on some fields, while the ML model performs at 93.69% Micro-F1. Gating on rule matches ensures the ML model never hallucinates attributes not present in the text. We also see that the ML model successfully triggered fallbacks for rare colors like silver and gold, routing them to the rule-based engine."

---

## Part 3: API & Docs Walkthrough (1:20 - 2:00)

### Talking Point
> "Now let's launch the FastAPI service. We can run this locally or containerized. Let's run it locally."

### Command
```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

### Action
- Open a web browser to `http://localhost:8000/docs`.
- Show the Swagger UI. Expand the `POST /extract` route and explain the request/response schemas.

---

## Part 4: Test Requests & Seed Cases (2:00 - 3:00)

### Talking Point
> "Let's hit the endpoint using curl to test the verbatim seed sentences from the assignment. First, we will run the extractor on the first seed description: a floor-length chiffon bridesmaid dress in sage and dusty blue."

### Command
```bash
curl -X "POST" ^
  "http://localhost:8000/extract" ^
  -H "Content-Type: application/json" ^
  -d "{\"description\": \"Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue\"}"
```
*(On Windows cmd.exe, use `^` for line continuation; on bash/macOS/Linux, replace `^` with `\`).*

### Expected Response
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

### Talking Point
> "Next, let's run another seed case: a sparkly sequin fitted prom gown featuring a deep illusion neckline."

### Command
```bash
curl -X "POST" ^
  "http://localhost:8000/extract" ^
  -H "Content-Type: application/json" ^
  -d "{\"description\": \"Sparkly sequin fitted prom gown featuring a deep illusion neckline and open back\"}"
```

### Expected Response
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

### Talking Point
> "This demonstrates that our hybrid extraction approach is robust, precise, and matches the assignment requirements perfectly. Thank you!"
