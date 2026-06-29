import os
from dataclasses import dataclass
from pathlib import Path

DATA_DIR_ENV_VAR = "AUDIOEXPLORER_DATA_DIR"



def get_data_dir() -> Path:
    return Path(os.environ[DATA_DIR_ENV_VAR])

