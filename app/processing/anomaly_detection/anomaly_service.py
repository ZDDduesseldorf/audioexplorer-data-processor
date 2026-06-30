from app.processing.anomaly_detection.detectors.isolation_forest_detector import (
    IsolationForestDetector,
)
# Import the Isolation Forest anomaly detector.

from app.processing.anomaly_detection.detectors.lof_detector import (
    LocalOutlierFactorDetector,
)
# Import the Local Outlier Factor anomaly detector.

from app.processing.anomaly_detection.anomaly_labeler import (
    AnomalyLabeler,
)
# Import the utility class for converting scores into anomaly labels.

from app.schemas.model import EmbeddingData
# Orchestrate the complete anomaly detection workflow by:
# - extracting embeddings
# - running Isolation Forest and LOF detectors
# - collecting anomaly scores
# - generating anomaly labels
# - returning structured results


# Define a service class responsible for coordinating anomaly detection.
class AnomalyService:
    # Calculate anomaly scores and labels for all provided embeddings.
    def calculate_anomalies(
        self,
        embeddings: list[EmbeddingData],
    ) -> dict:

        if embeddings is None:
            raise AttributeError("Embeddings cannot be None")

        # Extract all embedding vectors from the input dictionary.
        embedding_vectors = [item.embedding for item in embeddings]

        # Create an instance of the Isolation Forest detector.
        isolation_detector = IsolationForestDetector()

        # Create an instance of the Local Outlier Factor detector.
        lof_detector = LocalOutlierFactorDetector()

        # Run Isolation Forest anomaly detection on all embedding vectors.
        isolation_results = isolation_detector.fit_predict(embedding_vectors)

        # Run Local Outlier Factor anomaly detection on all embedding vectors.
        lof_results = lof_detector.fit_predict(embedding_vectors)

        # Create an empty dictionary for the final anomaly detection results.
        results = {}

        # Iterate through all embedding identifiers together with their index.
        for index, entry in enumerate(embeddings):
            # Retrieve the normalized Isolation Forest score for the current embedding.
            isolation_score = isolation_results[index]["normalized_score"]

            # Retrieve the normalized LOF score for the current embedding.
            lof_score = lof_results[index]["normalized_score"]

            # Create a result entry for the current embedding identifier.
            results[entry.uuid] = {
                "scores": {
                    "isolation_forest": round(
                        isolation_score,
                        2,
                    ),
                    "lof": round(
                        lof_score,
                        2,
                    ),
                },
                "labels": {
                    "isolation_forest": AnomalyLabeler.get_label(isolation_score),
                    "lof": AnomalyLabeler.get_label(lof_score),
                },
            }

        return results
