import json
from pathlib import Path


def load_json_file(file_path: Path) -> dict:
    """Load a JSON file from the given file path and return its contents as a dictionary."""
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def write_json_file(target_path: Path, data: dict):
    """Write the given data dictionary to a JSON file at the specified target path."""
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
