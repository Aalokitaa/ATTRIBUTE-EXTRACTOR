import os
import sys
# Add project root to path to resolve src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import numpy as np
from src.models.rule_based_extractor import RuleBasedExtractor
from src.models.ml_extractor import MLExtractor

def load_dataset(file_path):
    dataset = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                dataset.append(json.loads(line.strip()))
    return dataset

def compute_tp_fp_fn(true_val, pred_val, is_list=False):
    if is_list:
        true_set = set(true_val) if true_val else set()
        pred_set = set(pred_val) if pred_val else set()
        tp = len(true_set & pred_set)
        fp = len(pred_set - true_set)
        fn = len(true_set - pred_set)
    else:
        if true_val is not None and pred_val is not None:
            if true_val == pred_val:
                tp, fp, fn = 1, 0, 0
            else:
                tp, fp, fn = 0, 1, 1
        elif true_val is not None and pred_val is None:
            tp, fp, fn = 0, 0, 1
        elif true_val is None and pred_val is not None:
            tp, fp, fn = 0, 1, 0
        else: # Both None
            tp, fp, fn = 0, 0, 0
    return tp, fp, fn

def evaluate_extractor(extractor, dataset):
    attributes = ["Silhouette", "Fabric", "Neckline", "Sleeve", "Length", "Embellishment", "Color", "Category"]
    
    metrics = {attr: {"tp": 0, "fp": 0, "fn": 0, "correct": 0} for attr in attributes}
    total_examples = len(dataset)
    fallbacks_logged = []
    errors = []

    for idx, item in enumerate(dataset):
        desc = item["description"]
        pred = extractor.extract(desc)
        
        # Log fallbacks if they occurred (only MLExtractor will have fallback_triggered)
        if hasattr(extractor, "loaded") and extractor.loaded:
            for attr in attributes:
                msg = pred.get("fallback_triggered", {}).get(attr)
                if msg:
                    fallbacks_logged.append(f"Row {idx+1}: Field '{attr}' fallback triggered: {msg}")

        for attr in attributes:
            true_val = item[attr]
            pred_val = pred[attr]
            
            # Exact Match Accuracy check
            if attr == "Color":
                is_correct = sorted(true_val or []) == sorted(pred_val or [])
                tp, fp, fn = compute_tp_fp_fn(true_val, pred_val, is_list=True)
            else:
                is_correct = true_val == pred_val
                tp, fp, fn = compute_tp_fp_fn(true_val, pred_val, is_list=False)
                
            if is_correct:
                metrics[attr]["correct"] += 1
            else:
                errors.append({
                    "description": desc,
                    "attribute": attr,
                    "true": true_val,
                    "predicted": pred_val
                })
                
            metrics[attr]["tp"] += tp
            metrics[attr]["fp"] += fp
            metrics[attr]["fn"] += fn

    # Compute overall summary
    results = {}
    macro_f1_sum = 0
    total_tp = 0
    total_fp = 0
    total_fn = 0
    
    for attr in attributes:
        tp = metrics[attr]["tp"]
        fp = metrics[attr]["fp"]
        fn = metrics[attr]["fn"]
        correct = metrics[attr]["correct"]
        
        accuracy = correct / total_examples
        precision = tp / (tp + fp) if (tp + fp) > 0 else (1.0 if fn == 0 else 0.0)
        recall = tp / (tp + fn) if (tp + fn) > 0 else (1.0 if fp == 0 else 0.0)
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        macro_f1_sum += f1
        total_tp += tp
        total_fp += fp
        total_fn += fn
        
        results[attr] = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }
        
    macro_f1 = macro_f1_sum / len(attributes)
    micro_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    micro_f1 = 2 * micro_precision * micro_recall / (micro_precision + micro_recall) if (micro_precision + micro_recall) > 0 else 0.0
    
    return {
        "results": results,
        "micro_f1": micro_f1,
        "macro_f1": macro_f1,
        "errors": errors,
        "fallbacks": fallbacks_logged
    }

def main():
    test_path = os.path.join("data", "test.jsonl")
    if not os.path.exists(test_path):
        print("Test set not found. Please run src/train.py first.")
        return
        
    test_data = load_dataset(test_path)
    print(f"Loaded {len(test_data)} test examples.")
    
    rule_extractor = RuleBasedExtractor()
    ml_extractor = MLExtractor()
    
    rule_metrics = evaluate_extractor(rule_extractor, test_data)
    ml_metrics = evaluate_extractor(ml_extractor, test_data)
    
    attributes = ["Silhouette", "Fabric", "Neckline", "Sleeve", "Length", "Embellishment", "Color", "Category"]
    
    # Calculate support counts
    support_counts = {attr: 0 for attr in attributes}
    value_counts = {attr: {} for attr in attributes}
    for item in test_data:
        for attr in attributes:
            val = item.get(attr)
            if val is not None and val != [] and val != "":
                support_counts[attr] += 1
                if isinstance(val, list):
                    for v in val:
                        value_counts[attr][v] = value_counts[attr].get(v, 0) + 1
                else:
                    value_counts[attr][val] = value_counts[attr].get(val, 0) + 1

    # 1. Print Side-by-Side comparison to stdout
    print("\n" + "="*95)
    print(f"{'Attribute':<15} | {'Support (Non-Null)':<18} | {'Rule Accuracy':<13} | {'ML Accuracy':<11} | {'Rule F1':<9} | {'ML F1':<8}")
    print("="*95)
    
    for attr in attributes:
        r_acc = rule_metrics["results"][attr]["accuracy"]
        m_acc = ml_metrics["results"][attr]["accuracy"]
        r_f1 = rule_metrics["results"][attr]["f1"]
        m_f1 = ml_metrics["results"][attr]["f1"]
        support_str = f"{support_counts[attr]} / {len(test_data)}"
        print(f"{attr:<15} | {support_str:<18} | {r_acc:>12.2%}  | {m_acc:>10.2%}  | {r_f1:>8.2%}  | {m_f1:>7.2%}")
    print("="*95)
    print(f"Overall Rule-Based: Micro-F1 = {rule_metrics['micro_f1']:>.2%}, Macro-F1 = {rule_metrics['macro_f1']:>.2%}")
    print(f"Overall ML-Based:   Micro-F1 = {ml_metrics['micro_f1']:>.2%}, Macro-F1 = {ml_metrics['macro_f1']:>.2%}")
    print("="*95)
    
    # Report fallbacks
    print(f"\nTotal ML Fallbacks triggered in test set: {len(ml_metrics['fallbacks'])}")
    for fb in ml_metrics["fallbacks"][:5]:
        print(f"  - {fb}")
    if len(ml_metrics["fallbacks"]) > 5:
        print(f"  - ... and {len(ml_metrics['fallbacks']) - 5} more.")

    # Write evaluation comparison to EVALUATION.md in the workspace
    eval_md_content = f"""# Evaluation Report

This report evaluates and compares the performance of the **Rule-Based** and **ML-Based** product attribute extraction strategies on the held-out test split ({len(test_data)} examples).

## Summary Metrics (Side-by-Side)

| Attribute | Support (Non-Null) | Rule Accuracy | ML Accuracy | Rule F1-Score | ML F1-Score |
|---|---|---|---|---|---|
"""
    for attr in attributes:
        r_acc = rule_metrics["results"][attr]["accuracy"]
        m_acc = ml_metrics["results"][attr]["accuracy"]
        r_f1 = rule_metrics["results"][attr]["f1"]
        m_f1 = ml_metrics["results"][attr]["f1"]
        support_str = f"{support_counts[attr]} / {len(test_data)}"
        eval_md_content += f"| `{attr}` | {support_str} | {r_acc:.2%} | {m_acc:.2%} | {r_f1:.2%} | {m_f1:.2%} |\n"
        
    eval_md_content += f"""
### Overall Performance

| Strategy | Micro-F1 | Macro-F1 |
|---|---|---|
| **Rule-Based** | {rule_metrics['micro_f1']:.2%} | {rule_metrics['macro_f1']:.2%} |
| **ML-Based** | {ml_metrics['micro_f1']:.2%} | {ml_metrics['macro_f1']:.2%} |

---

## Detailed Test Set Support & Class Breakdown

This section lists the exact class-level and value-level support counts backing the evaluation metrics on the test split ({len(test_data)} examples total).

### Value-Level Occurrences
"""
    for attr in attributes:
        sorted_vals = sorted(value_counts[attr].items(), key=lambda x: x[1], reverse=True)
        vals_str = ", ".join([f"`{k}` ({v})" for k, v in sorted_vals]) if sorted_vals else "_None_"
        eval_md_content += f"- **{attr}** (Total non-null: {support_counts[attr]}): {vals_str}\n"

    eval_md_content += f"""
---

## ML Fallbacks Logged (Test Set)

Below are the logged cases where the ML model automatically fell back to the rule-based prediction because the target class/color had fewer than 3 training examples:

"""
    if ml_metrics["fallbacks"]:
        for fb in ml_metrics["fallbacks"]:
            eval_md_content += f"- {fb}\n"
    else:
        eval_md_content += "_No fallbacks were triggered on the test split._\n"

    # Identify worst performing ML fields
    ml_errors_by_attr = {}
    for err in ml_metrics["errors"]:
        attr = err["attribute"]
        ml_errors_by_attr[attr] = ml_errors_by_attr.get(attr, 0) + 1
    sorted_ml_errors = sorted(ml_errors_by_attr.items(), key=lambda x: x[1], reverse=True)

    eval_md_content += f"""
---

## ML Error & Failure Analysis

The 3 worst-performing fields for the ML model were:
"""
    for attr, count in sorted_ml_errors[:3]:
        eval_md_content += f"1. `{attr}`: {count} prediction error(s) in test set.\n"
        
    eval_md_content += """
### Qualitative Error Analysis
1. **Ambiguous Synonyms / Multi-words**: Phrases such as "illusion neckline" vs "V neckline" can confuse tokenizers, especially when small parts overlaps (e.g. "neckline").
2. **Implied Attributes**: Descriptions where an attribute is implied but not explicitly defined in the controlled vocabulary.
3. **Data Scarcity**: Even with rule-based features added, certain attributes with limited occurrences (1-2 times) are difficult to model reliably with machine learning classifiers, requiring robust fallback mechanisms.

### Future Recommendations
- **Transformer-based NER / Embeddings**: Using pre-trained contextual embeddings (such as SentenceTransformers or BERT) will improve the classification capability for rare synonyms.
- **Data Augmentation**: Generate synthetic product descriptions using template-based generation or LLMs to increase train size from 48 to 500+ examples.
"""

    eval_path = os.path.join(os.getcwd(), "EVALUATION.md")
    with open(eval_path, "w", encoding="utf-8") as f:
        f.write(eval_md_content)
    print(f"\nSaved detailed evaluation report to '{eval_path}'")

if __name__ == "__main__":
    main()
