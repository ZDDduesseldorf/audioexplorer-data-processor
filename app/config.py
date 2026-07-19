import os
from pathlib import Path

DATA_DIR_ENV_VAR = "AUDIOEXPLORER_DATA_DIR"
DEFAULT_DATA_DIR = "testdata"


def get_data_dir() -> Path:
    return Path(os.environ.get(DATA_DIR_ENV_VAR, DEFAULT_DATA_DIR))


def get_data_file_path(filename: str) -> Path:
    return get_data_dir() / filename


RAW_AUDIO_FOLDER = Path(
    os.environ.get(
        "AUDIOEXPLORER_RAW_AUDIO_FOLDER",
        get_data_dir() / "raw_audios",
    )
)

METADATA_FILENAME = "metadata.json"

TARGET_AUDIO_FOLDER = Path(
    os.environ.get(
        "AUDIOEXPLORER_TARGET_AUDIO_FOLDER",
        get_data_dir() / "processed_audios",
    )
)

TARGET_FILENAME_DATAOVERVIEW = "data_overview.npz"
TARGET_FILENAME_CATEGORYS = "category.npz"
