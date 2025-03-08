# app/services/reliability_score.py

def compute_reliability(support_count, refute_count, neutral_count):
    """
    Combine stance results into a single reliability percentage.
    """
    total = support_count + refute_count + neutral_count
    if total == 0:
        return 0.0
    score = (support_count - refute_count) / total
    # Shift from range [-1, 1] to [0, 100] or do your own weighting
    percentage = (score + 1) * 50
    return round(percentage, 2)
