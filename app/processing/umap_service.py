# Reduces a matrix of embeddings to 2D or 3D UMAP coordinates via PCA pre-reduction.

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from umap import UMAP

from app.schemas.model import EmbeddingData

_N_PCA_COMPONENTS: int = 50
_N_UMAP_NEIGHBORS: int = 15
_UMAP_MIN_DIST: float = 0.8


def calculate_umap_2d_from_list_embeddings(embeddings: list[EmbeddingData]):
    umap_results = {}

    embedding_matrix = np.vstack([entry.embedding for entry in embeddings])

    umap_coordinates = compute_umap_2d(embedding_matrix)

    for i, entry in enumerate(embeddings):
        umap_results[entry.uuid] = {
            "umap_x": float(umap_coordinates[i][0]),
            "umap_y": float(umap_coordinates[i][1]),
            "umap_z": 0,
        }

    return umap_results


def compute_umap_2d(embeddings: np.ndarray) -> np.ndarray:
    return _compute_umap(embeddings, n_components=2)


def compute_umap_3d(embeddings: np.ndarray) -> np.ndarray:
    return _compute_umap(embeddings, n_components=3)


def _compute_umap(embeddings: np.ndarray, n_components: int) -> np.ndarray:
    scaled = _scale(embeddings)
    pca_result = _apply_pca(scaled)
    return _apply_umap(pca_result, n_components)


def _scale(embeddings: np.ndarray) -> np.ndarray:
    result: np.ndarray = StandardScaler().fit_transform(embeddings)
    return result


def _apply_pca(scaled: np.ndarray) -> np.ndarray:
    n_components = min(_N_PCA_COMPONENTS, scaled.shape[0] - 1, scaled.shape[1])
    result: np.ndarray = PCA(n_components=n_components, random_state=1).fit_transform(
        scaled
    )
    return result


def _apply_umap(reduced: np.ndarray, n_components: int) -> np.ndarray:
    n_neighbors = min(_N_UMAP_NEIGHBORS, reduced.shape[0] - 1)
    result: np.ndarray = UMAP(
        n_components=n_components,
        n_neighbors=n_neighbors,
        min_dist=_UMAP_MIN_DIST,
        init="random",
        random_state=1,
    ).fit_transform(reduced)
    return result
