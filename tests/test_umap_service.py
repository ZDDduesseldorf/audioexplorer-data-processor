import numpy as np

from app.processing.umap_service import (
    _apply_pca,
    _scale,
    compute_umap_2d,
    compute_umap_3d,
)


def _fake_embeddings(n: int, dims: int = 512) -> np.ndarray:
    rng = np.random.default_rng(1)
    return rng.standard_normal((n, dims)).astype(np.float32)


def test_scaling_does_not_change_shape() -> None:
    embeddings = _fake_embeddings(20)
    result = _scale(embeddings)
    assert result.shape == embeddings.shape


def test_scaling_produces_near_zero_mean() -> None:
    embeddings = _fake_embeddings(50)
    result = _scale(embeddings)
    assert abs(float(result.mean())) < 0.1


def test_pca_output_has_at_most_50_components() -> None:
    scaled = _scale(_fake_embeddings(60))
    result = _apply_pca(scaled)
    assert result.shape[0] == 60
    assert result.shape[1] <= 50


def test_2d_umap_output_has_two_coordinates_per_sample() -> None:
    embeddings = _fake_embeddings(60)
    result = compute_umap_2d(embeddings)
    assert result.shape == (60, 2)


def test_3d_umap_output_has_three_coordinates_per_sample() -> None:
    embeddings = _fake_embeddings(60)
    result = compute_umap_3d(embeddings)
    assert result.shape == (60, 3)


def test_2d_umap_works_with_few_samples() -> None:
    embeddings = _fake_embeddings(5)
    result = compute_umap_2d(embeddings)
    assert result.shape == (5, 2)


def test_3d_umap_works_with_few_samples() -> None:
    embeddings = _fake_embeddings(5)
    result = compute_umap_3d(embeddings)
    assert result.shape == (5, 3)
