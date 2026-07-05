import contextlib
from unittest.mock import MagicMock, patch

import numpy as np

from app.processing.embeddings.embedding_service import (
    compute_embedding,
    compute_embeddings_batch,
)


def _mock_manager(embedding_shape: tuple[int, int] = (1, 512)) -> MagicMock:
    manager = MagicMock()
    fake_pooler_output = MagicMock()
    fake_pooler_output.cpu.return_value.numpy.return_value = np.zeros(
        embedding_shape,
        dtype=np.float32,
    )

    fake_features = MagicMock()
    fake_features.pooler_output = fake_pooler_output
    manager.model.get_audio_features.return_value = fake_features
    return manager


@patch(
    "app.processing.embeddings.embedding_service.torch.no_grad",
    return_value=contextlib.nullcontext(),
)
def test_single_embedding_has_correct_shape(mock_no_grad: MagicMock) -> None:
    manager = _mock_manager()
    waveform = np.zeros(48000, dtype=np.float32)

    result = compute_embedding(waveform, manager)

    assert result.shape == (512,)


@patch(
    "app.processing.embeddings.embedding_service.torch.no_grad",
    return_value=contextlib.nullcontext(),
)
def test_model_is_called_during_embedding(mock_no_grad: MagicMock) -> None:
    manager = _mock_manager()
    waveform = np.zeros(48000, dtype=np.float32)

    compute_embedding(waveform, manager)

    manager.model.get_audio_features.assert_called_once()


@patch(
    "app.processing.embeddings.embedding_service.torch.no_grad",
    return_value=contextlib.nullcontext(),
)
def test_batch_output_has_one_row_per_waveform(mock_no_grad: MagicMock) -> None:
    manager = _mock_manager()
    waveforms = [np.zeros(48000, dtype=np.float32) for _ in range(4)]

    result = compute_embeddings_batch(waveforms, manager)

    assert result.shape == (4, 512)
