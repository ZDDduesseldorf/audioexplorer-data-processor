import numpy as np

from app.processing.audio.filter import (
    AudioLengthFilter,
    AudioNoiseReducer,
    AudioSilenceFilter,
)


def test_length_filter_accepts_valid_audio_length() -> None:
    audio = np.zeros(48_000)

    result = AudioLengthFilter().is_valid(
        audio=audio,
        sample_rate=48_000,
        min_duration_seconds=0.5,
        max_duration_seconds=2.0,
    )

    assert result is True


def test_length_filter_rejects_too_short_audio() -> None:
    audio = np.zeros(8_000)

    result = AudioLengthFilter().is_valid(
        audio=audio,
        sample_rate=48_000,
        min_duration_seconds=1.0,
        max_duration_seconds=2.0,
    )

    assert result is False


def test_length_filter_rejects_too_long_audio() -> None:
    audio = np.zeros(144_000)

    result = AudioLengthFilter().is_valid(
        audio=audio,
        sample_rate=48_000,
        min_duration_seconds=1.0,
        max_duration_seconds=2.0,
    )

    assert result is False


def test_silence_filter_rejects_silent_audio() -> None:
    audio = np.zeros(48_000)

    result = AudioSilenceFilter().is_valid(
        audio=audio,
        silence_rms_threshold=0.005,
    )

    assert result is False


def test_silence_filter_accepts_audio_with_signal() -> None:
    audio = np.ones(48_000) * 0.01

    result = AudioSilenceFilter().is_valid(
        audio=audio,
        silence_rms_threshold=0.005,
    )

    assert result is True


def test_noise_reducer_does_not_change_shape() -> None:
    audio = np.array([0.001, 0.01, -0.02, 0.0005], dtype=np.float32)

    result = AudioNoiseReducer().reduce_noise(
        audio=audio,
        noise_reduction_strength=1.0,
    )

    assert result.shape == audio.shape


def test_noise_reducer_keeps_dtype() -> None:
    audio = np.array([0.001, 0.01, -0.02, 0.0005], dtype=np.float32)

    result = AudioNoiseReducer().reduce_noise(
        audio=audio,
        noise_reduction_strength=1.0,
    )

    assert result.dtype == audio.dtype
