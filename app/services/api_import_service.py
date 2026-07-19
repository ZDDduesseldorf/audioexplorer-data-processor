from pathlib import Path

import requests


def import_categories(npz_file: Path) -> None:
    with npz_file.open("rb") as f:
        response = requests.post(
            "http://host.docker.internal:8000/api/v1/imports/categories",
            files={"file": f},
            timeout=60,
        )

    response.raise_for_status()
    print(response.json())


def import_data_overview(npz_file: Path) -> None:
    with npz_file.open("rb") as f:
        response = requests.post(
            "http://host.docker.internal:8000/api/v1/imports/data-overview",
            files={"file": f},
            timeout=60,
        )

    response.raise_for_status()
    print(response.json())
