from pathlib import Path

import requests


def import_categories(npz_file: Path) -> None:
    """Import category data into the backend.

    Uploads a compressed NPZ file containing category information to the
    backend import endpoint.

    Args:
        npz_file: Path to the NPZ file containing the category data.

    Raises:
        requests.HTTPError: If the backend returns an unsuccessful HTTP
            status code.
    """
    with npz_file.open("rb") as f:
        response = requests.post(
            "http://host.docker.internal:8000/api/v1/imports/categories",
            files={"file": f},
            timeout=60,
        )

    response.raise_for_status()
    print(response.json())


def import_data_overview(npz_file: Path) -> None:
    """Import DataOverview data into the backend.

    Uploads a compressed NPZ file containing DataOverview information to the
    backend import endpoint.

    Args:
        npz_file: Path to the NPZ file containing the DataOverview data.

    Raises:
        requests.HTTPError: If the backend returns an unsuccessful HTTP
            status code.
    """
    with npz_file.open("rb") as f:
        response = requests.post(
            "http://host.docker.internal:8000/api/v1/imports/data-overview",
            files={"file": f},
            timeout=60,
        )

    response.raise_for_status()
    print(response.json())
