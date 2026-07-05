import numpy as np
# Import NumPy and use the alias 'np' for numerical calculations.

# Normalize anomaly scores using Min-Max scaling.
# The smallest score becomes 0 and the largest score becomes 100.
# All other scores are scaled proportionally within that range.


# Define a function that scales anomaly scores to a range between 0 and 100.
def normalize_scores(scores):

    # Find the smallest score in the input array.
    min_score = np.min(scores)

    # Find the largest score in the input array.
    max_score = np.max(scores)

    # Check if all scores are identical to avoid division by zero.
    if max_score - min_score == 0:
        # Return an array of zeros because normalization is not possible when all values are equal.
        return np.zeros(len(scores))

    # Apply Min-Max normalization and scale the values to the range 0-100.
    normalized = ((scores - min_score) / (max_score - min_score)) * 100

    return normalized

    # Return the normalized scores as a NumPy array.
