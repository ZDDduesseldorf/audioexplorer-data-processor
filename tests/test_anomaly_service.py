import pytest
import numpy as np

from app.processing.anomaly_detection.anomaly_service import (
    AnomalyService,
)
from app.schemas.model import EmbeddingData


def test_calculate_anomalies_returns_result_for_valid_embeddings():
    """
    Verify successful anomaly detection for valid embeddings.

    Goal:
        Ensure that the anomaly service can process multiple
        embedding vectors and return anomaly scores and labels.

    Covered code:
        - anomaly_service.py
            calculate_anomalies()
        - isolation_forest_detector.py
            fit_predict()
        - lof_detector.py
            fit_predict()
        - anomaly_labeler.py
            get_label()

    Why this test matters:
        This is the primary use case of the anomaly detection
        pipeline and verifies that valid embeddings produce
        valid anomaly results.
    """

    # Create anomaly service instance

    service = AnomalyService()

    # Create valid sample embeddings

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

    # Execute anomaly detection

    results = service.calculate_anomalies(embeddings)

    # Verify that results exist for all embeddings

    assert len(results) == 3

    assert "audio_001" in results

    # Verify generated output structure

    assert "scores" in results["audio_001"]

    assert "labels" in results["audio_001"]


def test_calculate_anomalies_raises_for_empty_dictionary():
    """
    Verify behaviour for an empty embedding dictionary.

    Goal:
        Ensure that anomaly detection rejects datasets
        without embeddings.

    Covered code:
        - validation.py
        - detector validation logic

    Why this test matters:
        Running anomaly detection on an empty dataset
        would produce meaningless results and should
        fail immediately.
    """

    # Create anomaly service instance

    service = AnomalyService()

    # Verify that an exception is raised

    with pytest.raises(ValueError):
        service.calculate_anomalies({})


def test_calculate_anomalies_raises_for_none():
    """
    Verify behaviour when None is passed as input.

    Goal:
        Ensure that missing embedding data is rejected.

    Covered code:
        - anomaly_service.py
            embeddings.keys()

    Why this test matters:
        None values may occur because of loading failures,
        API errors or pipeline integration issues.

        The system should fail instead of producing
        invalid anomaly results.
    """

    # Create anomaly service instance

    service = AnomalyService()

    # Verify exception for missing input

    with pytest.raises(AttributeError):
        service.calculate_anomalies(None)


def test_calculate_anomalies_raises_for_empty_embedding():
    """
    Verify behaviour for empty embedding vectors.

    Goal:
        Ensure that every embedding contains at least
        one numerical feature.

    Covered code:
        - validation.py
            if len(embedding) == 0

    Why this test matters:
        Machine learning models cannot operate on
        empty vectors.
    """

    # Create anomaly service instance

    service = AnomalyService()

    # Create invalid embedding

    embeddings = [
        EmbeddingData(
            uuid="audio_001",
            embedding=np.array([]),
        )
    ]

    # Verify exception

    with pytest.raises(ValueError):
        service.calculate_anomalies(embeddings)


def test_calculate_anomalies_raises_for_non_numeric_values():
    """
    Verify behaviour for embeddings containing
    non-numeric values.

    Goal:
        Ensure that only numerical vectors are accepted.

    Covered code:
        - validation.py
            if not isinstance(value, (int, float))

    Why this test matters:
        Scikit-learn algorithms require numerical
        feature vectors.

        Invalid values must be detected before
        model execution.
    """

    # Create anomaly service instance

    service = AnomalyService()

    # Create invalid embedding containing a string

    embeddings = [
        EmbeddingData(
            uuid="audio_001",
            embedding=np.array([0.1, "invalid", 0.3]),
        )
    ]

    # Verify exception

    with pytest.raises(TypeError):
        service.calculate_anomalies(embeddings)


def test_calculate_anomalies_raises_for_non_list_embedding():
    """
    Verify behaviour when an embedding is not stored
    as a list.

    Goal:
        Ensure that every embedding follows the
        expected vector format.

    Covered code:
        - validation.py
            if not isinstance(embedding, list)

    Why this test matters:
        The anomaly detection algorithms expect
        embeddings to be vectors represented as
        Python lists.

        Any other structure should be rejected.
    """

    # Create anomaly service instance

    service = AnomalyService()

    # Create invalid embedding format

    embeddings = [
        EmbeddingData(
            uuid="audio_001",
            embedding=np.array(["not_a_vector"]),
        )
    ]

    # Verify exception

    with pytest.raises(TypeError):
        service.calculate_anomalies(embeddings)
