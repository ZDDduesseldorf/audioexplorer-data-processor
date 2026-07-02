from pathlib import Path
from unittest.mock import patch

import numpy as np


from app.processing.audio.loader import LocalAudioLoader

TEST_SAMPLE_RATE = 48_000


@patch("app.processing.audio.loader.librosa.load")
def test_output_is_float32(mock_load: object) -> None:
    mock_load.return_value = (  # type: ignore[attr-defined]
        np.zeros(TEST_SAMPLE_RATE, dtype=np.float64),
        TEST_SAMPLE_RATE,
    )

    audio, _ = LocalAudioLoader().load(Path("test.wav"))

    assert audio.dtype == np.float32


@patch("app.processing.audio.loader.librosa.load")
def test_librosa_is_called_with_correct_sample_rate_and_mono(mock_load: object) -> None:
    mock_load.return_value = (np.zeros(100, dtype=np.float32), TEST_SAMPLE_RATE)  # type: ignore[attr-defined]

    LocalAudioLoader().load(Path("audio.wav"))

    mock_load.assert_called_once_with(  # type: ignore[attr-defined]
        str(Path("audio.wav")), sr=None, mono=True
    )


@patch("app.processing.audio.loader.librosa.load")
def test_waveform_length_is_unchanged(mock_load: object) -> None:
    expected = np.ones(TEST_SAMPLE_RATE, dtype=np.float32)
    mock_load.return_value = (expected, TEST_SAMPLE_RATE)  # type: ignore[attr-defined]

    result, _ = LocalAudioLoader().load(Path("audio.wav"))

    assert result.shape == (TEST_SAMPLE_RATE,)


@patch("app.processing.audio.loader.librosa.load")
def test_local_audio_loader_returns_waveform_and_sample_rate(mock_load: object) -> None:
    expected_audio = np.ones(TEST_SAMPLE_RATE, dtype=np.float32)
    mock_load.return_value = (expected_audio, TEST_SAMPLE_RATE)  # type: ignore[attr-defined]

    audio, sample_rate = LocalAudioLoader().load(Path("audio.wav"))

    assert audio.shape == (TEST_SAMPLE_RATE,)
    assert sample_rate == TEST_SAMPLE_RATE
