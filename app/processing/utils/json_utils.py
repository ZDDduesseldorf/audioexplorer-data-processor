import json
from pathlib import Path
from app.config import get_data_file_path
from app.schemas.model import CategoryListItem


def load_json_file(file_path: Path) -> dict:
    """Load a JSON file from the given file path and return its contents as a dictionary."""
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def write_json_file(target_path: Path, data: dict):
    """Write the given data dictionary to a JSON file at the specified target path."""
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_all_categories() -> list[CategoryListItem]:
    """Load all categories from the category_list.json file and return a list of CategoryListItem objects."""
    json_path = get_data_file_path("category_list.json")

    data_json = load_json_file(json_path)

    return [
        CategoryListItem(id=id, key=item["key"], name=item["displayName"])
        for id, item in data_json.items()
    ]
