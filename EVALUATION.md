# Evaluation Report

This report evaluates and compares the performance of the **Rule-Based** and **ML-Based** product attribute extraction strategies on the held-out test split (12 examples).

## Summary Metrics (Side-by-Side)

| Attribute | Support (Non-Null) | Rule Accuracy | ML Accuracy | Rule F1-Score | ML F1-Score |
|---|---|---|---|---|---|
| `Silhouette` | 3 / 12 | 100.00% | 100.00% | 100.00% | 100.00% |
| `Fabric` | 10 / 12 | 100.00% | 100.00% | 100.00% | 100.00% |
| `Neckline` | 9 / 12 | 100.00% | 83.33% | 100.00% | 87.50% |
| `Sleeve` | 6 / 12 | 100.00% | 91.67% | 100.00% | 90.91% |
| `Length` | 9 / 12 | 100.00% | 91.67% | 100.00% | 94.12% |
| `Embellishment` | 5 / 12 | 100.00% | 91.67% | 100.00% | 88.89% |
| `Color` | 7 / 12 | 91.67% | 91.67% | 94.12% | 94.12% |
| `Category` | 8 / 12 | 91.67% | 91.67% | 93.33% | 93.33% |

### Overall Performance

| Strategy | Micro-F1 | Macro-F1 |
|---|---|---|
| **Rule-Based** | 98.28% | 98.43% |
| **ML-Based** | 93.69% | 93.61% |

---

## Detailed Test Set Support & Class Breakdown

This section lists the exact class-level and value-level support counts backing the evaluation metrics on the test split (12 examples total).

### Value-Level Occurrences
- **Silhouette** (Total non-null: 3): `sheath` (2), `ball gown` (1)
- **Fabric** (Total non-null: 10): `sequin` (3), `satin` (2), `jersey` (2), `lace` (1), `chiffon` (1), `velvet` (1)
- **Neckline** (Total non-null: 9): `illusion` (3), `sweetheart` (2), `off shoulder` (2), `one shoulder` (1), `square` (1)
- **Sleeve** (Total non-null: 6): `strapless` (2), `puff sleeve` (2), `long sleeve` (1), `sleeveless` (1)
- **Length** (Total non-null: 9): `high slit` (4), `sweep train` (3), `short` (2)
- **Embellishment** (Total non-null: 5): `sequin` (3), `ruched` (1), `feather trim` (1)
- **Color** (Total non-null: 7): `royal navy` (2), `silver` (2), `ivory` (1), `white` (1), `black` (1), `rose gold` (1)
- **Category** (Total non-null: 8): `wedding dress` (2), `prom gown` (2), `evening gown` (2), `cocktail dress` (2)

---

## ML Fallbacks Logged (Test Set)

Below are the logged cases where the ML model automatically fell back to the rule-based prediction because the target class/color had fewer than 3 training examples:

- Row 4: Field 'Color' fallback triggered: Colors ['silver'] have < 3 training examples. Fell back to rule-based.
- Row 8: Field 'Color' fallback triggered: Colors ['silver'] have < 3 training examples. Fell back to rule-based.
- Row 12: Field 'Color' fallback triggered: Colors ['rose gold', 'gold'] have < 3 training examples. Fell back to rule-based.

---

## ML Error & Failure Analysis

The 3 worst-performing fields for the ML model were:
1. `Neckline`: 2 prediction error(s) in test set.
1. `Embellishment`: 1 prediction error(s) in test set.
1. `Length`: 1 prediction error(s) in test set.

### Qualitative Error Analysis
1. **Ambiguous Synonyms / Multi-words**: Phrases such as "illusion neckline" vs "V neckline" can confuse tokenizers, especially when small parts overlaps (e.g. "neckline").
2. **Implied Attributes**: Descriptions where an attribute is implied but not explicitly defined in the controlled vocabulary.
3. **Data Scarcity**: Even with rule-based features added, certain attributes with limited occurrences (1-2 times) are difficult to model reliably with machine learning classifiers, requiring robust fallback mechanisms.

### Future Recommendations
- **Transformer-based NER / Embeddings**: Using pre-trained contextual embeddings (such as SentenceTransformers or BERT) will improve the classification capability for rare synonyms.
- **Data Augmentation**: Generate synthetic product descriptions using template-based generation or LLMs to increase train size from 48 to 500+ examples.
