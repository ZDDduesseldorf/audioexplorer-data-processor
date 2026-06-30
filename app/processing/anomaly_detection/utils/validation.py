import numpy as np
# Validate embeddings before anomaly detection.


# Validate that the embeddings input has the expected structure and data types.
def validate_embeddings(embeddings):

    # Check whether the embeddings object is None.
    if embeddings is None:
        raise ValueError("Embeddings cannot be None")
        # Raise an error because embeddings must contain data.

    if len(embeddings) == 0:
        raise ValueError("Embeddings cannot be empty")

    # Verify that the embeddings object is a Python list.
    if not isinstance(embeddings, list):
        # Raise an error because embeddings must be provided as a list.
        raise TypeError("Embeddings must be a list")

    # Iterate through each embedding vector in the embeddings list.
    for embedding in embeddings:
        # Verify that each embedding is represented as a numpyarray.
        if not isinstance(embedding, np.ndarray):
            # Raise an error if an embedding is not a numpyarray.
            raise TypeError("Each embedding must be a numpyarray")

        # Check whether the embedding vector is empty.
        if embedding.size == 0:
            # Raise an error because every embedding must contain values.
            raise ValueError("Embedding vector cannot be empty")

        # Verify that every embedding value is numeric.
        if not np.issubdtype(embedding.dtype, np.number):
            # Raise an error if a value is not an integer or floating-point number.
            raise TypeError("Embedding values must be numeric")
