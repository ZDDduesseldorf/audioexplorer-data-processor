from pathlib import Path

import librosa
import numpy as np


class LocalAudioLoader:
    def load(self, file_path: Path) -> tuple[np.ndarray, int]:
        audio, sample_rate = librosa.load(
            str(file_path),
            sr=None,
            mono=True,
        )

        return audio, int(sample_rate)


# TODO: DatabaseAudioLoader
