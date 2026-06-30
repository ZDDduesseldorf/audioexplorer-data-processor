import pytest
import numpy as np

from app.processing.anomaly_detection.utils.validation import (
    validate_embeddings,
)


def test_validate_embeddings_raises_for_none():
    """
    Verify that validation rejects None input.

    Goal:
        Ensure that embeddings cannot be None.

    Covered code:
        validation.py
        if embeddings is None:
            raise ValueError(...)

    Why this test matters:
        Prevents the anomaly detection pipeline from
        processing missing embedding data.
    """

    with pytest.raises(ValueError):
        validate_embeddings(None)


def test_validate_embeddings_accepts_valid_embeddings():
    embeddings = [
        np.array([1.0, 2.0, 3.0]),
        np.array([4.0, 5.0, 6.0]),
    ]

    validate_embeddings(embeddings)


def test_validate_embeddings_raises_for_empty_list():
    with pytest.raises(ValueError):
        validate_embeddings([])


def test_validate_embeddings_raises_for_non_list():
    with pytest.raises(TypeError):
        validate_embeddings("invalid")


def test_validate_embeddings_raises_for_non_list_embedding():
    with pytest.raises(TypeError):
        validate_embeddings(
            [
                "not_a_vector",
            ]
        )


def test_validate_embeddings_raises_for_empty_embedding():
    with pytest.raises(ValueError):
        validate_embeddings(
            [
                np.array([]),
            ]
        )


def test_validate_embeddings_raises_for_non_numeric_value():
    with pytest.raises(TypeError):
        validate_embeddings(
            [
                [1.0, "invalid", 3.0],
            ]
        )
