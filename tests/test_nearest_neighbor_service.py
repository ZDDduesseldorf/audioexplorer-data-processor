import numpy as np

from app.schemas.model import EmbeddingData
from app.processing.nearest_neighbor_service import (
    _compute_neighbor_matrix,
    compute_nearest_neighbors,
)


def _fake_embeddings(n: int, dims: int = 512) -> list[EmbeddingData]:
    rng = np.random.default_rng(1)
    return [
        EmbeddingData(
            uuid=str(i), embedding=rng.standard_normal(dims).astype(np.float32)
        )
        for i in range(n)
    ]


def test_returns_one_entry_per_uuid() -> None:
    embeddings = _fake_embeddings(40)
    result = compute_nearest_neighbors(embeddings, k=30)
    assert set(result.keys()) == {str(i) for i in range(40)}


def test_returns_k_neighbors_per_uuid() -> None:
    embeddings = _fake_embeddings(40)
    result = compute_nearest_neighbors(embeddings, k=30)
    for neighbors in result.values():
        assert len(neighbors) == 30


def test_neighbor_entries_map_uuid_to_float_distance() -> None:
    embeddings = _fake_embeddings(10)
    result = compute_nearest_neighbors(embeddings, k=5)
    for neighbor_uuid, distance in result["0"].items():
        assert isinstance(neighbor_uuid, str)
        assert isinstance(distance, float)


def test_point_itself_is_excluded_from_its_neighbors() -> None:
    embeddings = _fake_embeddings(10)
    result = compute_nearest_neighbors(embeddings, k=5)
    for uuid, neighbors in result.items():
        assert uuid not in neighbors


def test_neighbors_are_ordered_by_ascending_distance() -> None:
    embeddings = _fake_embeddings(20)
    result = compute_nearest_neighbors(embeddings, k=10)
    distances = list(result["0"].values())
    assert distances == sorted(distances)


def test_cosine_distance_is_within_valid_range() -> None:
    embeddings = _fake_embeddings(20)
    result = compute_nearest_neighbors(embeddings, k=10)
    for neighbors in result.values():
        for distance in neighbors.values():
            assert 0.0 <= distance <= 2.0


def test_works_when_k_exceeds_available_samples() -> None:
    embeddings = _fake_embeddings(5)
    result = compute_nearest_neighbors(embeddings, k=30)
    # only 4 other points exist besides the point itself
    for neighbors in result.values():
        assert len(neighbors) == 4


def test_neighbor_matrix_includes_the_point_itself() -> None:
    matrix = np.vstack([e.embedding for e in _fake_embeddings(15)])
    distances, indices = _compute_neighbor_matrix(matrix, k=5)
    assert distances.shape == (15, 6)
    assert indices.shape == (15, 6)
    # first neighbor of each point is itself with distance ~0.0
    for i in range(15):
        assert indices[i][0] == i
        assert distances[i][0] < 1e-6
