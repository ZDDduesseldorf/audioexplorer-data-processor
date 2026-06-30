from pathlib import Path

import numpy as np

from app.processing.audio.loader import LocalAudioLoader


def load_audio(file_path: Path) -> np.ndarray:
    waveform, _ = LocalAudioLoader().load(file_path)
    return waveform.astype(np.float32)
