"""
ROUGE Evaluation Module
Computes ROUGE-1, ROUGE-2, ROUGE-L, ROUGE-LSum scores.
Enhanced with text preprocessing and multi-reference support for better accuracy.
"""

import re
from rouge_score import rouge_scorer


def _preprocess_text(text: str) -> str:
    """
    Preprocess text before ROUGE computation for better accuracy.
    - Normalize whitespace and line breaks
    - Lowercase (handled by use_stemmer)
    - Remove excessive punctuation noise
    """
    # Normalize line breaks so paragraph boundaries are respected
    text = re.sub(r'\r\n|\r', '\n', text)
    # Collapse 3+ newlines to 2 (preserve paragraph structure for rougeLsum)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def compute_rouge_scores(reference: str, hypothesis: str) -> dict:
    """
    Compute ROUGE scores between reference and hypothesis texts.
    Returns ROUGE-1, ROUGE-2, ROUGE-L, ROUGE-LSum with precision, recall, and F1.

    Higher accuracy by:
    - Using both rougeL and rougeLsum (sentence-aware LCS)
    - use_stemmer=True for morphological normalization
    - Text preprocessing for fair comparison
    """
    if not reference or not hypothesis:
        return _empty_scores()

    reference = _preprocess_text(reference)
    hypothesis = _preprocess_text(hypothesis)

    scorer = rouge_scorer.RougeScorer(
        ['rouge1', 'rouge2', 'rougeL', 'rougeLsum'],
        use_stemmer=True   # Porter stemmer — normalizes run/running/ran → run
    )

    scores = scorer.score(reference, hypothesis)

    return {
        "rouge1": {
            "precision": round(scores['rouge1'].precision, 4),
            "recall":    round(scores['rouge1'].recall, 4),
            "f1":        round(scores['rouge1'].fmeasure, 4),
        },
        "rouge2": {
            "precision": round(scores['rouge2'].precision, 4),
            "recall":    round(scores['rouge2'].recall, 4),
            "f1":        round(scores['rouge2'].fmeasure, 4),
        },
        "rougeL": {
            "precision": round(scores['rougeL'].precision, 4),
            "recall":    round(scores['rougeL'].recall, 4),
            "f1":        round(scores['rougeL'].fmeasure, 4),
        },
        "rougeLsum": {
            "precision": round(scores['rougeLsum'].precision, 4),
            "recall":    round(scores['rougeLsum'].recall, 4),
            "f1":        round(scores['rougeLsum'].fmeasure, 4),
        },
    }


def compute_rouge_multi_reference(references: list, hypothesis: str) -> dict:
    """
    Compute ROUGE against multiple reference texts and return best scores per metric.
    Useful when the model has multiple candidate ground-truth summaries.
    """
    if not references or not hypothesis:
        return _empty_scores()

    best = {}
    for ref in references:
        scores = compute_rouge_scores(ref, hypothesis)
        for metric, vals in scores.items():
            if metric not in best or vals["f1"] > best[metric]["f1"]:
                best[metric] = vals

    return best


def _empty_scores() -> dict:
    """Return zero scores when inputs are invalid."""
    empty = {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    return {
        "rouge1":    dict(empty),
        "rouge2":    dict(empty),
        "rougeL":    dict(empty),
        "rougeLsum": dict(empty),
    }


def format_rouge_display(scores: dict) -> str:
    """Format ROUGE scores for display."""
    lines = []
    for metric, values in scores.items():
        lines.append(
            f"{metric.upper()}: F1={values['f1']:.4f} "
            f"(P={values['precision']:.4f}, R={values['recall']:.4f})"
        )
    return " | ".join(lines)
