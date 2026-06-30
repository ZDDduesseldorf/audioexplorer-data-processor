import os
from pathlib import Path

DATA_DIR_ENV_VAR = "AUDIOEXPLORER_DATA_DIR"
DEFAULT_DATA_DIR = "testdata"


def get_data_dir() -> Path:
    return Path(os.environ.get(DATA_DIR_ENV_VAR, DEFAULT_DATA_DIR))


def get_data_file_path(filename: str) -> Path:
    return get_data_dir() / filename
