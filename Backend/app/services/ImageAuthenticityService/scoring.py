def compute_realness_score(results):
    """
    results might be a dict containing:
      {
        "exif_score": float,
        "reverse_search_score": float,
        "ai_prob": float,  # Probability image is AI
        "deepfake_score": float,
        "ela_score": float,
        ...
      }
    We combine them into a single "Realness Score" (0 to 100).
    """
    # Weighted example:
    exif_weight = 1.0
    reverse_weight = 1.0
    ai_weight = 2.0       # If ai_prob is high, penalize
    deepfake_weight = 1.0
    ela_weight = 1.0

    # Convert AI probability to a "realness" factor (the more AI_prob, the less real)
    # e.g., realness_from_ai = (1 - ai_prob)
    realness_from_ai = (1 - results["ai_prob"])

    # Weighted sum (each sub-score is out of 1.0 for simplicity)
    raw_score = (
        exif_weight * results["exif_score"] +
        reverse_weight * results["reverse_search_score"] +
        ai_weight * realness_from_ai +
        deepfake_weight * results["deepfake_score"] +
        ela_weight * results["ela_score"]
    )

    # Possible maximum = exif_weight + reverse_weight + ai_weight + deepfake_weight + ela_weight
    max_score = exif_weight + reverse_weight + ai_weight + deepfake_weight + ela_weight

    final_realness = (raw_score / max_score) * 100
    return round(final_realness, 2)
