# import logging
# OPTIONAL: Import Python's logging module for recording informational messages.


# Import NumPy and use the alias 'np' for numerical operations.
# Import the Local Outlier Factor algorithm from scikit-learn
# for anomaly detection.
import numpy as np
from sklearn.neighbors import LocalOutlierFactor  # type: ignore

# Import the abstract base detector class that defines the detector interface.
from app.processing.anomaly_detection.detectors.base_detector import (
    BaseDetector,
)

# Import detector configuration values.
from app.processing.anomaly_detection.utils.detector_config import (
    DetectorConfig,
)

# Import the utility function used to normalize anomaly scores.
from app.processing.anomaly_detection.utils.normalization import (
    normalize_scores,
)

# Import the validation function for checking embedding inputs.
from app.processing.anomaly_detection.utils.validation import (
    validate_embeddings,
)

# OPTIONAL: Logger
# Create a logger instance for this module.
# logger = logging.getLogger(__name__)

# This detector uses the Local Outlier Factor algorithm to identify anomalies,
# normalizes the resulting outlier scores to a 0-100 range,
# and returns structured anomaly detection results.


# Define an anomaly detector based on the Local Outlier Factor algorithm.
# from abstract class BaseDetector
class LocalOutlierFactorDetector(BaseDetector):
    # Initialize the detector with LOF configuration parameters.
    def __init__(
        self,
        contamination=DetectorConfig.LOF["contamination"],
        n_neighbors=DetectorConfig.LOF["n_neighbors"],
        metric=DetectorConfig.LOF["metric"],
    ):

        # Create and configure a Local Outlier Factor model instance.
        # The configirations are configured in the other file
        # SEE: detector_config.py
        self.model = LocalOutlierFactor(
            contamination=contamination,
            n_neighbors=n_neighbors,
            metric=metric,
        )

    # Run anomaly detection on the provided
    # embeddings and return the results.
    def fit_predict(self, embeddings):

        # Verify that the embeddings are valid before processing.
        validate_embeddings(embeddings)

        # OPTIONAL: LOGGER
        # Log that the Local Outlier Factor detection process has started.
        # logger.info("Running LOF detection")

        # Convert the embeddings into a NumPy array.
        embeddings_np = np.array(embeddings)

        # Fit the LOF model and calculate outlier predictions for all embeddings.
        self.model.fit_predict(embeddings_np)

        # Retrieve the raw LOF anomaly scores from the trained model.
        raw_scores = self.model.negative_outlier_factor_

        # Invert and normalize the LOF scores so that larger values indicate stronger anomalies.
        normalized_scores = normalize_scores(-raw_scores)

        # Create an empty list for storing anomaly detection results.
        results = []

        # Iterate through all normalized scores and their indices.
        for idx, score in enumerate(normalized_scores):
            # Add a result entry for the current embedding.
            results.append(
                {
                    "embedding_index": idx,
                    # Store the index of the embedding in the original dataset.
                    "algorithm": "Local Outlier Factor",
                    "raw_score": float(raw_scores[idx]),
                    # Store the original LOF score before normalization.
                    "normalized_score": round(float(score), 2),
                    # Store the normalized anomaly score rounded to two decimal places.
                }
            )

        return results
