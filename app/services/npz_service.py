import numpy as np
from pathlib import Path

from app.schemas.model import DataOverviewJSON, CategoryListItem


def create_npz_file_from_category_list_json(
    list_categorys: list[CategoryListItem], target_path: Path
):
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
        filenames=np.array(
            [data.filename for data in dataoverview],
            dtype="U255",
        ),
        sources=np.array(
            [data.source for data in dataoverview],
            dtype="U100",
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
            [data.nearest_neighbors for data in dataoverview],
            dtype="U1000",
        ),
    )

    print(f"Created {target_path}")
