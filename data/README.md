# Dataset Documentation

This directory contains the labeled dataset for the fashion/apparel product attribute extraction task.

## Dataset Files
- `labeled_dataset.jsonl`: The full set of 60 manually labeled product descriptions.
- `train.jsonl`: Training split (80% or 48 examples).
- `test.jsonl`: Held-out testing split (20% or 12 examples).

## Split Methodology
- Split logic is implemented in `src/generate_data.py` with a fixed random seed of `42`.
- It uses a standard 80/20 train/test split.

## Label Schema

Each example contains a `description` field and 8 target attributes. The target attributes use a controlled vocabulary (defined in `src/vocabulary.py`):

| Attribute | Type | Allowed Values (Ontology) | Description |
|---|---|---|---|
| `silhouette` | string / null | A-line, mermaid, ball gown, sheath, fit and flare | The shape or silhouette of the dress. |
| `fabric` | string / null | chiffon, satin, lace, tulle, velvet, sequin, jersey | The primary material/fabric used. |
| `neckline` | string / null | V neck, sweetheart, off shoulder, square, illusion, one shoulder | The style of the neckline. |
| `sleeve` | string / null | long sleeve, cap sleeve, puff sleeve, sleeveless, strapless | The type/length of sleeves. |
| `length` | string / null | floor length, short, mini, sweep train, high slit | The length of the skirt/dress or train details. |
| `embellishment` | string / null | beaded, sequin, embroidery, feather trim, ruched, pleated | The decoration/embellishment on the dress. |
| `color` | list | sage, dusty blue, royal navy, emerald, black, white, ivory, red, gold, silver, rose gold, blush, champagne, lavender, burgundy, plum | A list of colors appearing in the description. |
| `category` | string / null | bridesmaid dress, prom gown, wedding dress, cocktail dress, evening gown | The product category/occasion classification. |

## Annotation & Matching Guidelines
- **Strictly No Hallucination**: If an attribute is not explicitly mentioned or clearly synonymous (e.g. "navy blue" matching "royal navy"), it is set to `null` (or an empty list `[]` for `color`).
- **Single-value Fields**: If multiple values are co-occurring (e.g. both "floor length" and "high slit" are present), a single primary value is annotated based on what dominates or is closest to the focus. The models are trained to extract one value for these fields.
- **Multi-value Fields**: `color` is a list and can contain multiple items if the description details several options (e.g., "available in sage and dusty blue" -> `["sage", "dusty blue"]`).
