from pathlib import Path
from uuid import UUID

import numpy as np
import soundfile as sf  # type: ignore[import-untyped]


class AudioSaver:
    def save(
        self,
        audio: np.ndarray,
        sample_rate: int,
        source_path: Path,
        output_dir: Path,
    ) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        audio_uuid = self.extract_uuid_from_filename(source_path)
        output_path = output_dir / f"{audio_uuid}.wav"

        # atomic save
        tmp_output_path = output_path.with_suffix(".wav.tmp")

        try:
            if tmp_output_path.exists():
                tmp_output_path.unlink()

            sf.write(
                file=str(tmp_output_path),
                data=audio,
                samplerate=sample_rate,
                format="WAV",
            )

            self._validate_saved_audio(
                path=tmp_output_path,
                expected_sample_rate=sample_rate,
            )

            tmp_output_path.replace(output_path)

            return output_path

        except Exception:
            if tmp_output_path.exists():
                tmp_output_path.unlink()

            raise

    def _validate_saved_audio(
        self,
        path: Path,
        expected_sample_rate: int,
    ) -> None:
        if not path.exists():
            raise FileNotFoundError(f"Saved audio file does not exist: {path}")

        if path.stat().st_size == 0:
            raise ValueError(f"Saved audio file is empty: {path}")

        info = sf.info(str(path))

        if info.frames <= 0:
            raise ValueError(f"Saved audio file contains no frames: {path}")

        if info.samplerate != expected_sample_rate:
            raise ValueError(
                f"Saved audio sample rate mismatch: expected {expected_sample_rate}, got {info.samplerate}"
            )

    def extract_uuid_from_filename(self, source_path: Path) -> str:
        filename_without_extension = source_path.stem

        try:
            UUID(filename_without_extension)
        except ValueError:
            return filename_without_extension

        return filename_without_extension
