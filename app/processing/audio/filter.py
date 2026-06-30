import numpy as np


class AudioLengthFilter:
    def is_valid(
        self,
        audio: np.ndarray,
        sample_rate: int,
        min_duration_seconds: float,
        max_duration_seconds: float | None,
    ) -> bool:
        duration_seconds = len(audio) / sample_rate

        if duration_seconds < min_duration_seconds:
            return False

        if max_duration_seconds is not None and duration_seconds > max_duration_seconds:
            return False

        return True


class AudioSilenceFilter:
    def is_valid(
        self,
        audio: np.ndarray,
        silence_rms_threshold: float,
    ) -> bool:
        rms_energy = float(np.sqrt(np.mean(audio**2)))

        return rms_energy >= silence_rms_threshold


class AudioNoiseReducer:
    def reduce_noise(
        self,
        audio: np.ndarray,
        noise_reduction_strength: float,
    ) -> np.ndarray:
        if audio.size == 0:
            return audio

        noise_level = float(np.percentile(np.abs(audio), 20))
        threshold = noise_level * noise_reduction_strength

        reduced_audio = np.where(
            np.abs(audio) < threshold,
            0.0,
            audio,
        )

        return reduced_audio.astype(audio.dtype)
