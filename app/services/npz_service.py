import json
from pathlib import Path

import numpy as np

from app.schemas.model import CategoryListItem, DataOverviewJSON


def create_npz_file_from_category_list_json(
    list_categorys: list[CategoryListItem], target_path: Path
):
    """Store category information as a compressed NPZ file.

    Converts a list of ``CategoryListItem`` objects into NumPy arrays and
    saves them as a compressed NPZ file.

    Args:
        list_categorys: List of category objects to store.
        target_path: Path of the output NPZ file.
    """
    np.savez_compressed(
        target_path,
        ids=np.array(
            [category.id for category in list_categorys],
            dtype=np.int64,
        ),
        category_keys=np.array(
            [category.key for category in list_categorys],
            dtype="U100",
        ),
        display_names=np.array(
            [category.name for category in list_categorys],
            dtype="U100",
        ),
    )

    print(f"Created {target_path}")


def create_npz_file_from_list_DataOverview(
    dataoverview: list[DataOverviewJSON], target_path: Path
):
    """Store DataOverview objects as a compressed NPZ file.

    Converts a list of ``DataOverviewJSON`` objects into NumPy arrays and
    stores the contained metadata, UMAP coordinates, anomaly scores, labels,
    nearest-neighbor information, and additional information in a compressed
    NPZ file.

    Complex fields such as ``additional_information`` and
    ``nearest_neighbors`` are serialized as JSON strings before being stored.

    Args:
        dataoverview: List of DataOverview objects to serialize.
        target_path: Path of the output NPZ file.
    """
    np.savez_compressed(
        target_path,
        uuids=np.array(
            [data.uuid for data in dataoverview],
            dtype="U36",
        ),
        umap=np.array(
            [[data.umap_x, data.umap_y, data.umap_z] for data in dataoverview],
            dtype=np.float64,
        ),
        labels=np.array(
            [data.label for data in dataoverview],
            dtype="U100",
        ),
        category_keys=np.array(
            [data.category for data in dataoverview],
            dtype="U100",
        ),
        original_filenames=np.array(
            [data.original_filename for data in dataoverview],
            dtype="U255",
        ),
        sources=np.array(
            [data.source for data in dataoverview],
            dtype="U100",
        ),
        additional_information=np.array(
            [json.dumps(data.additional_information) for data in dataoverview],
            dtype="U10000",
        ),
        anomalie_isolation_forest=np.array(
            [data.anomalie_isolation_forest for data in dataoverview],
            dtype=np.float64,
        ),
        anomalie_lof=np.array(
            [data.anomalie_LOF for data in dataoverview],
            dtype=np.float64,
        ),
        anomalie_lof_labels=np.array(
            [data.anomalie_LOF_label for data in dataoverview],
            dtype="U100",
        ),
        anomalie_isolation_forest_labels=np.array(
            [data.anomalie_isolation_forest_label for data in dataoverview],
            dtype="U100",
        ),
        nearest_neighbors=np.array(
            [
                json.dumps(
                    data.nearest_neighbors,
                    ensure_ascii=False,
                )
                for data in dataoverview
            ],
            dtype="U10000",
        ),
    )

    print(f"Created {target_path}")
