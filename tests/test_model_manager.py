import pytest
from unittest.mock import MagicMock, patch

from app.processing.embeddings.model_manager import ModelManager


def test_not_loaded_at_start() -> None:
    manager = ModelManager()
    assert manager.is_loaded is False


def test_accessing_model_without_load_raises_error() -> None:
    manager = ModelManager()
    with pytest.raises(RuntimeError, match="Call load()"):
        _ = manager.model


def test_accessing_processor_without_load_raises_error() -> None:
    manager = ModelManager()
    with pytest.raises(RuntimeError, match="Call load()"):
        _ = manager.processor


@patch("app.processing.embeddings.model_manager.ClapProcessor")
@patch("app.processing.model_manager.ClapModel")
def test_load_downloads_model_and_marks_as_loaded(
    mock_model_cls: MagicMock, mock_processor_cls: MagicMock
) -> None:
    mock_model = MagicMock()
    mock_model_cls.from_pretrained.return_value = mock_model
    mock_processor_cls.from_pretrained.return_value = MagicMock()

    manager = ModelManager()
    manager.load()

    assert manager.is_loaded is True
    mock_model.eval.assert_called_once()


@patch("app.processing.embeddings.model_manager.ClapProcessor")
@patch("app.processing.embeddings.model_manager.ClapModel")
def test_load_twice_downloads_model_only_once(
    mock_model_cls: MagicMock, mock_processor_cls: MagicMock
) -> None:
    mock_model_cls.from_pretrained.return_value = MagicMock()
    mock_processor_cls.from_pretrained.return_value = MagicMock()

    manager = ModelManager()
    manager.load()
    manager.load()

    mock_model_cls.from_pretrained.assert_called_once()
