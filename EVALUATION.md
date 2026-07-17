# Evaluation Report

This report evaluates and compares the performance of the **Rule-Based** and **ML-Based** product attribute extraction strategies on the held-out test split (15 examples).

## Summary Metrics (Side-by-Side)

| Attribute | Support (Non-Null) | Rule Accuracy | ML Accuracy | Rule F1-Score | ML F1-Score |
|---|---|---|---|---|---|
| `Silhouette` | 8 / 15 | 100.00% | 86.67% | 100.00% | 85.71% |
| `Fabric` | 14 / 15 | 93.33% | 93.33% | 92.86% | 92.86% |
| `Neckline` | 10 / 15 | 100.00% | 93.33% | 100.00% | 90.00% |
| `Sleeve` | 8 / 15 | 100.00% | 93.33% | 100.00% | 93.33% |
| `Length` | 10 / 15 | 100.00% | 93.33% | 100.00% | 94.74% |
| `Embellishment` | 7 / 15 | 100.00% | 100.00% | 100.00% | 100.00% |
| `Color` | 11 / 15 | 93.33% | 93.33% | 96.00% | 96.00% |
| `Category` | 15 / 15 | 86.67% | 73.33% | 92.86% | 78.57% |

### Overall Performance

| Strategy | Micro-F1 | Macro-F1 |
|---|---|---|
| **Rule-Based** | 97.01% | 97.71% |
| **ML-Based** | 90.80% | 91.40% |

---

## Detailed Test Set Support & Class Breakdown

This section lists the exact class-level and value-level support counts backing the evaluation metrics on the test split (15 examples total).

### Value-Level Occurrences
- **Silhouette** (Total non-null: 8): `mermaid` (3), `A-line` (2), `ball gown` (2), `fit and flare` (1)
- **Fabric** (Total non-null: 14): `lace` (4), `satin` (3), `sequin` (2), `chiffon` (2), `velvet` (2), `tulle` (1)
- **Neckline** (Total non-null: 10): `off shoulder` (3), `sweetheart` (3), `illusion` (1), `V neck` (1), `one shoulder` (1), `square` (1)
- **Sleeve** (Total non-null: 8): `long sleeve` (3), `cap sleeve` (2), `sleeveless` (1), `strapless` (1), `puff sleeve` (1)
- **Length** (Total non-null: 10): `sweep train` (4), `short` (2), `high slit` (2), `ankle length` (1), `floor length` (1)
- **Embellishment** (Total non-null: 7): `sequin` (3), `pleated` (2), `feather trim` (1), `embroidery` (1)
- **Color** (Total non-null: 11): `white` (2), `royal navy` (2), `pink` (1), `purple` (1), `red` (1), `lavender` (1), `gold` (1), `silver` (1), `dusty blue` (1), `black` (1)
- **Category** (Total non-null: 15): `evening gown` (6), `prom gown` (4), `wedding dress` (3), `cocktail dress` (1), `bridesmaid dress` (1)

---

## ML Fallbacks Logged (Test Set)

Below are the logged cases where the ML model automatically fell back to the rule-based prediction because the target class/color had fewer than 3 training examples:

- Row 1: Field 'Length' fallback triggered: Class 'ankle length' has < 3 training examples. Fell back to rule-based.
- Row 1: Field 'Color' fallback triggered: Colors ['pink'] have < 3 training examples. Fell back to rule-based.
- Row 7: Field 'Color' fallback triggered: Colors ['lavender'] have < 3 training examples. Fell back to rule-based.
- Row 9: Field 'Color' fallback triggered: Colors ['gold'] have < 3 training examples. Fell back to rule-based.
- Row 11: Field 'Color' fallback triggered: Colors ['blue'] have < 3 training examples. Fell back to rule-based.
- Row 12: Field 'Silhouette' fallback triggered: Class 'fit and flare' has < 3 training examples. Fell back to rule-based.

---

## ML Error & Failure Analysis

The 3 worst-performing fields for the ML model were:
1. `Category`: 4 prediction error(s) in test set.
1. `Silhouette`: 2 prediction error(s) in test set.
1. `Sleeve`: 1 prediction error(s) in test set.

### Qualitative Error Analysis
1. **Ambiguous Synonyms / Multi-words**: Phrases such as "illusion neckline" vs "V neckline" can confuse tokenizers, especially when small parts overlaps (e.g. "neckline").
2. **Implied Attributes**: Descriptions where an attribute is implied but not explicitly defined in the controlled vocabulary.
3. **Data Scarcity**: Even with rule-based features added, certain attributes with limited occurrences (1-2 times) are difficult to model reliably with machine learning classifiers, requiring robust fallback mechanisms.

### Future Recommendations
- **Transformer-based NER / Embeddings**: Using pre-trained contextual embeddings (such as SentenceTransformers or BERT) will improve the classification capability for rare synonyms.
- **Data Augmentation**: Generate synthetic product descriptions using template-based generation or LLMs to increase train size from 48 to 500+ examples.
