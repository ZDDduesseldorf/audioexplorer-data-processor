import numpy as np

from app.processing.audio.resampler import AudioResampler


def test_resampler_does_not_change_audio_when_sample_rate_matches() -> None:
    audio = np.ones(16_000, dtype=np.float32)

    result = AudioResampler().resample(
        audio=audio,
        original_sample_rate=16_000,
        target_sample_rate=16_000,
    )

    assert np.array_equal(result, audio)


def test_resampler_changes_audio_length_when_sample_rate_changes() -> None:
    audio = np.ones(8_000, dtype=np.float32)

    result = AudioResampler().resample(
        audio=audio,
        original_sample_rate=8_000,
        target_sample_rate=16_000,
    )

    assert result.shape[0] == 16_000


def test_resampler_returns_numpy_array() -> None:
    audio = np.ones(8_000, dtype=np.float32)

    result = AudioResampler().resample(
        audio=audio,
        original_sample_rate=8_000,
        target_sample_rate=16_000,
    )

    assert isinstance(result, np.ndarray)
