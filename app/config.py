import os
from dataclasses import dataclass
from pathlib import Path

DATA_DIR_ENV_VAR = "AUDIOEXPLORER_DATA_DIR"

DB_CONNECTION_STRING_ENV_VAR = "DB_CONNECTION_STRING"
DB_HOST_ENV_VAR = "DB_HOST"
DB_PORT_ENV_VAR = "DB_PORT"
DB_NAME_ENV_VAR = "DB_NAME"
DB_USER_ENV_VAR = "DB_USER"
DB_PASSWORD_ENV_VAR = "DB_PASSWORD"


@dataclass(frozen=True)
class DatabaseConfig:
    connection_string: str
    host: str
    port: int
    name: str
    user: str
    password: str


def get_data_dir() -> Path:
    return Path(os.environ[DATA_DIR_ENV_VAR])


def get_database_config() -> DatabaseConfig:
    return DatabaseConfig(
        connection_string=os.environ[DB_CONNECTION_STRING_ENV_VAR],
        host=os.environ[DB_HOST_ENV_VAR],
        port=int(os.environ[DB_PORT_ENV_VAR]),
        name=os.environ[DB_NAME_ENV_VAR],
        user=os.environ[DB_USER_ENV_VAR],
        password=os.environ[DB_PASSWORD_ENV_VAR],
    )
