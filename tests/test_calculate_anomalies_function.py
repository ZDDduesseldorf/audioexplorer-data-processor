import numpy as np
from app.schemas.model import EmbeddingData
from app.processing.anomaly_detection.anomaly_service import (
    AnomalyService,
)

# LOCAL TEST:
# PYTHONPATH=. pytest tests/test_calculate_anomalies_function.py -v
#
# Unit test for the calculate_anomalies() method.
#

# Expected output:
# Each embedding should contain:
# - Isolation Forest score
# - Local Outlier Factor score
# - Isolation Forest label
# - Local Outlier Factor label


def test_calculate_anomalies_accepts_embedding_dictionary():
    """
    Verify successful anomaly detection for a valid embedding dictionary.

    Goal:
        Ensure that calculate_anomalies() accepts a dictionary
        containing multiple embedding vectors and produces
        anomaly scores and labels for every embedding.

    Covered code:
        - anomaly_service.py
            calculate_anomalies()
        - isolation_forest_detector.py
            fit_predict()
        - lof_detector.py
            fit_predict()
        - anomaly_labeler.py
            get_label()
        - validation.py
            validate_embeddings()
        - normalization.py
            normalize_scores()

    What is being validated:
        - A dictionary is returned.
        - Every input embedding ID exists in the result.
        - Scores are generated for Isolation Forest and LOF.
        - Labels are generated for Isolation Forest and LOF.
        - Score values are floats.
        - Label values are strings.
        - Normalized scores stay within the expected 0-100 range.

    Why this test matters:
        This is the primary business use case of the anomaly
        detection module. It verifies that the complete anomaly
        detection pipeline works correctly from input embeddings
        to final scores and labels.

        The same result structure will later be consumed by
        downstream analysis components and frontend visualizations.
    """

    # Create a dictionary exactly like the one
    # that will later be produced by the embedding pipeline

    embeddings = [
        EmbeddingData(
            uuid="audio_001",
            embedding=np.array([0.1, 0.2, 0.3]),
        ),
        EmbeddingData(
            uuid="audio_002",
            embedding=np.array([1.1, 1.2, 1.3]),
        ),
        EmbeddingData(
            uuid="audio_003",
            embedding=np.array([2.1, 2.2, 2.3]),
        ),
    ]

    # Create the anomaly service

    service = AnomalyService()

    # Run anomaly detection on all embeddings

    results = service.calculate_anomalies(embeddings)

    # Verify that a dictionary is returned

    assert isinstance(
        results,
        dict,
    )

    # Verify that all input IDs are present
    # in the output

    assert "audio_001" in results
    assert "audio_002" in results
    assert "audio_003" in results

    # Verify output structure for one audio sample

    sample = results["audio_001"]

    assert "scores" in sample
    assert "labels" in sample

    # Verify score fields

    assert "isolation_forest" in sample["scores"]

    assert "lof" in sample["scores"]

    # Verify label fields

    assert "isolation_forest" in sample["labels"]

    assert "lof" in sample["labels"]

    # Verify score data types

    assert isinstance(
        sample["scores"]["isolation_forest"],
        float,
    )

    assert isinstance(
        sample["scores"]["lof"],
        float,
    )

    # Verify label data types

    assert isinstance(
        sample["labels"]["isolation_forest"],
        str,
    )

    assert isinstance(
        sample["labels"]["lof"],
        str,
    )

    # Verify score range after normalization

    assert 0 <= sample["scores"]["isolation_forest"] <= 100

    assert 0 <= sample["scores"]["lof"] <= 100
