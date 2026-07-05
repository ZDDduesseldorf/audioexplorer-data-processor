# CONVERTING ANOMALY SCORES
# INTO HUMAN-READABLE LABELS

# Scores are categorized into:
# - Not Anomalous (0<20.00)
# - Slightly Anomalous (20.00<50.00)
# - Anomalous (50.00<80.00)
# - Highly Anomalous (80.00-100.00)


class AnomalyLabeler:
    NOT_ANOMALOUS = "Not Anomalous"
    # Label for scores indicating normal behavior.
    SLIGHTLY_ANOMALOUS = "Slightly Anomalous"
    # Label for scores indicating a small degree of anomaly.
    ANOMALOUS = "Anomalous"
    # Label for scores indicating a clear anomaly.
    HIGHLY_ANOMALOUS = "Highly Anomalous"
    # Label for scores indicating a strong anomaly.

    # Convert a normalized anomaly score into a descriptive anomaly label.
    @staticmethod
    def get_label(score: float) -> str:

        # Verify that the anomaly score is within the valid range of 0 to 100.
        if score < 0 or score > 100:
            raise ValueError("Anomaly score must be between 0 and 100")

        # Check whether the score falls into the normal range.
        if score < 20.00:
            return AnomalyLabeler.NOT_ANOMALOUS

        # Check whether the score falls into the slightly anomalous range.
        if score < 50.00:
            return AnomalyLabeler.SLIGHTLY_ANOMALOUS

        # Check whether the score falls into the anomalous range.
        if score < 80.00:
            return AnomalyLabeler.ANOMALOUS

        # Return the label for highly anomalous data.
        return AnomalyLabeler.HIGHLY_ANOMALOUS

    # Generate anomaly labels for Isolation Forest and Local Outlier Factor scores.
    @staticmethod
    def create_labels(isolation_score: float, lof_score: float) -> dict:

        # Return a dictionary containing labels for both anomaly detection algorithms.
        # Convert the Isolation Forest score into a descriptive label.
        # Convert the Local Outlier Factor score into a descriptive label.

        return {
            "isolation_forest_label": AnomalyLabeler.get_label(isolation_score),
            "local_outlier_factor_label": AnomalyLabeler.get_label(lof_score),
        }
