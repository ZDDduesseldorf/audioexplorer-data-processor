import numpy as np

from app.processing.anomaly_detection.utils.normalization import (
    normalize_scores,
)


def test_normalize_scores_returns_zeroes_when_all_scores_equal():
    """
    Verify normalization behaviour when all scores are identical.

    Goal:
        Ensure division-by-zero is avoided.

    Covered code:
        normalization.py
        if max_score - min_score == 0:
            return np.zeros(...)

    Why this test matters:
        All embeddings may receive the same anomaly score.
        The normalization must remain stable and return
        valid output instead of crashing.
    """

    scores = np.array([5, 5, 5, 5])

    normalized = normalize_scores(scores)

    assert np.array_equal(
        normalized,
        np.array([0, 0, 0, 0]),
    )


def test_normalize_scores_returns_percentages():

    scores = np.array([10, 20, 30])

    normalized = normalize_scores(scores)

    assert normalized[0] == 0
    assert normalized[1] == 50
    assert normalized[2] == 100
