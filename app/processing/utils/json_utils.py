import json
from pathlib import Path

from app.config import get_data_file_path
from app.schemas.model import CategoryListItem


def load_json_file(file_path: Path) -> dict:
    """Load a JSON file.

    Reads the JSON file at the specified path and returns its contents as a
    dictionary.

    Args:
        file_path: Path to the JSON file.

    Returns:
        The parsed JSON content.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def write_json_file(target_path: Path, data: dict):
    """Write data to a JSON file.

    Serializes the given dictionary as JSON and writes it to the specified
    file using UTF-8 encoding.

    Args:
        target_path: Path to the output JSON file.
        data: Dictionary to serialize.
    """
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_all_categories() -> list[CategoryListItem]:
    """Load all available categories.

    Reads the ``category_list.json`` file and converts its entries into a
    list of ``CategoryListItem`` objects.

    Returns:
        A list of available categories.
    """
    json_path = get_data_file_path("category_list.json")

    data_json = load_json_file(json_path)

    return [
        CategoryListItem(id=id, key=item["key"], name=item["displayName"])
        for id, item in data_json.items()
    ]
