from pathlib import Path

import numpy as np

from app.processing.audio.saver import AudioSaver


def test_saver_saves_audio_file(tmp_path: Path) -> None:
    source_path = tmp_path / "550e8400-e29b-41d4-a716-446655440000.wav"
    output_dir = tmp_path / "processed"
    audio = np.ones(16_000, dtype=np.float32) * 0.01

    saved_path = AudioSaver().save(
        audio=audio,
        sample_rate=16_000,
        source_path=source_path,
        output_dir=output_dir,
    )

    assert saved_path.exists()


def test_saver_uses_uuid_from_filename(tmp_path: Path) -> None:
    source_path = tmp_path / "550e8400-e29b-41d4-a716-446655440000.wav"
    output_dir = tmp_path / "processed"
    audio = np.ones(16_000, dtype=np.float32) * 0.01

    saved_path = AudioSaver().save(
        audio=audio,
        sample_rate=16_000,
        source_path=source_path,
        output_dir=output_dir,
    )

    assert saved_path.name == "550e8400-e29b-41d4-a716-446655440000.wav"


def test_saver_uses_filename_when_no_uuid_exists(tmp_path: Path) -> None:
    source_path = tmp_path / "test_audio.wav"
    output_dir = tmp_path / "processed"
    audio = np.ones(16_000, dtype=np.float32) * 0.01

    saved_path = AudioSaver().save(
        audio=audio,
        sample_rate=16_000,
        source_path=source_path,
        output_dir=output_dir,
    )

    assert saved_path.name == "test_audio.wav"


def test_saver_creates_output_directory(tmp_path: Path) -> None:
    source_path = tmp_path / "550e8400-e29b-41d4-a716-446655440000.wav"
    output_dir = tmp_path / "nested" / "processed"
    audio = np.ones(16_000, dtype=np.float32) * 0.01

    saved_path = AudioSaver().save(
        audio=audio,
        sample_rate=16_000,
        source_path=source_path,
        output_dir=output_dir,
    )

    assert output_dir.exists()
    assert saved_path.exists()
