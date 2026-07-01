# import logging

# OPTIONAL: Import Python's logging module for recording
# informational and debug messages.

# Import NumPy and use the alias 'np'
# for numerical and array operations.
import numpy as np


# Import the Isolation Forest algorithm from
# scikit-learn for anomaly detection.
from sklearn.ensemble import IsolationForest

# Import the abstract base detector class that
# defines the common detector interface.
from app.processing.anomaly_detection.detectors.base_detector import (
    BaseDetector,
)

# Import configuration values used to initialize the detector.
from app.processing.anomaly_detection.utils.detector_config import (
    DetectorConfig,
)

# Import the utility function used to scale anomaly scores to a 0-100 range.
from app.processing.anomaly_detection.utils.normalization import (
    normalize_scores,
)

# Import the validation function to ensure embeddings are valid before processing.
from app.processing.anomaly_detection.utils.validation import (
    validate_embeddings,
)

# OPTIONAL: LOGGER
# logger = logging.getLogger(__name__)


# Define an anomaly detector based on the Isolation Forest algorithm.

# This detector trains an Isolation Forest model, computes anomaly scores,
# normalizes them to a 0-100 range, and returns structured detection results.


class IsolationForestDetector(BaseDetector):
    def __init__(
        self,
        contamination=DetectorConfig.ISOLATION_FOREST["contamination"],
        n_estimators=DetectorConfig.ISOLATION_FOREST["n_estimators"],
        random_state=DetectorConfig.ISOLATION_FOREST["random_state"],
        # Initialize the detector with configuration values or custom parameters.
    ):
        self.model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=random_state,
        )

    # Create and configure an Isolation Forest model instance.

    # Train the model on embeddings and return anomaly detection results.
    def fit_predict(self, embeddings):

        # Verify that the input embeddings are
        # valid and properly formatted.
        validate_embeddings(embeddings)

        # Optional: if we need a logger
        # Write an informational log message indicating that detection has started.
        # logger.info("Running Isolation Forest detection")

        # Convert the embeddings into a NumPy array for scikit-learn compatibility.
        embeddings_np = np.array(embeddings)

        # THE MOST IMPORTANT PART
        # Train the Isolation Forest model using the embedding vectors.
        self.model.fit(embeddings_np)

        # Calculate anomaly scores for all embeddings using the trained model.
        decision_scores = self.model.decision_function(embeddings_np)

        # Invert and normalize the scores so that higher values indicate stronger anomalies.
        normalized_scores = normalize_scores(-decision_scores)

        # Create an empty list to store anomaly detection results.
        results = []

        # Iterate through all normalized scores together with their indices.
        for idx, score in enumerate(normalized_scores):
            # Add the current detection result to the results list.
            results.append(
                {
                    "embedding_index": idx,
                    "algorithm": "Isolation Forest",
                    "raw_score": float(decision_scores[idx]),
                    "normalized_score": round(float(score), 2),
                    # Store the normalized anomaly score ROUNDED to
                    # two decimal places.
                }
            )

        return results
