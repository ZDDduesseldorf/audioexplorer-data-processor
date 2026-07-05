# Computes the k nearest neighbors per embedding using cosine distance.

import numpy as np
from sklearn.neighbors import NearestNeighbors

from app.schemas.model import EmbeddingData

_DEFAULT_K: int = 30


def compute_nearest_neighbors(
    embeddings: list[EmbeddingData], k: int = _DEFAULT_K
) -> dict[str, dict[str, float]]:
    """Compute the k nearest neighbors per embedding via cosine distance.

    Returns a mapping of uuid to its nearest neighbors as ``{neighbor_uuid: distance}``,
    ordered by ascending distance (0.0 = identical, 1.0 = maximally different).
    """

    uuids = [entry.uuid for entry in embeddings]
    embedding_matrix = np.vstack([entry.embedding for entry in embeddings])

    distances, indices = _compute_neighbor_matrix(embedding_matrix, k)

    result: dict[str, dict[str, float]] = {}

    for i, uuid in enumerate(uuids):
        neighbors: dict[str, float] = {}

        for rank in range(1, len(indices[i])):
            neighbor_index = indices[i][rank]
            neighbor_uuid = uuids[neighbor_index]
            neighbors[neighbor_uuid] = round(float(distances[i][rank]), 5)

        result[uuid] = neighbors

    return result


def _compute_neighbor_matrix(
    embeddings: np.ndarray, k: int
) -> tuple[np.ndarray, np.ndarray]:
    n_neighbors = min(k + 1, embeddings.shape[0])
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine").fit(embeddings)
    return nbrs.kneighbors(embeddings)
