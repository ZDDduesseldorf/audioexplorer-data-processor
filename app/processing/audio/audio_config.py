from dataclasses import dataclass
# from pathlib import Path


@dataclass
class AudioPreprocessingConfig:
    # input_dir: Path = Path("data/nvv_clips")
    # output_dir: Path = Path("data/nvv_clips_preprocessed")

    target_sample_rate: int = 48_000  # match Model Requirements

    apply_length_filter: bool = True
    min_duration_seconds: float = 0.1
    max_duration_seconds: float | None = 30.0

    apply_silence_filter: bool = True
    silence_rms_threshold: float = 0.005

    apply_noise_reduction: bool = True
    noise_reduction_strength: float = 1.0
