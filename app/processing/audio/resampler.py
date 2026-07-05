import librosa
import numpy as np


class AudioResampler:
    def resample(
        self,
        audio: np.ndarray,
        original_sample_rate: int,
        target_sample_rate: int,
    ) -> np.ndarray:
        if original_sample_rate == target_sample_rate:
            return audio

        return librosa.resample(
            y=audio,
            orig_sr=original_sample_rate,
            target_sr=target_sample_rate,
        )
