import pytest

from app.processing.anomaly_detection.anomaly_labeler import (
    AnomalyLabeler,
)


def test_returns_highly_anomal():
    """
    Verify label assignment for audio samples.

    Goal:
        Ensure scores are
        classified correctly.

    Covered code:
        anomaly_labeler.py

    Why this test matters:
        Correct label classification is essential
        for anomaly analysis.
    """

    assert AnomalyLabeler.get_label(90) == "Highly Anomalous"


def test_returns_not_anomal():

    assert AnomalyLabeler.get_label(10) == "Not Anomalous"


def test_returns_slightly_anomal():

    assert AnomalyLabeler.get_label(30) == "Slightly Anomalous"


def test_returns_anomal():

    assert AnomalyLabeler.get_label(70) == "Anomalous"


def test_raises_for_negative_score():

    with pytest.raises(ValueError):
        AnomalyLabeler.get_label(-1)


def test_raises_for_score_above_100():

    with pytest.raises(ValueError):
        AnomalyLabeler.get_label(101)
