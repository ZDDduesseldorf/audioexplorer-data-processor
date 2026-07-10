# tests/test_npz_export.py

from types import SimpleNamespace

import numpy as np
import pytest

from app.services.npz_service import (
    create_npz_file_from_category_list_json,
    create_npz_file_from_list_DataOverview,
)


def test_create_npz_file_from_category_list_json(tmp_path, capsys):
    categories = [
        SimpleNamespace(id=1, key="cat_a", name="Kategorie A"),
        SimpleNamespace(id=2, key="cat_b", name="Kategorie B"),
    ]
    target_path = tmp_path / "categories.npz"

    create_npz_file_from_category_list_json(categories, target_path)

    assert target_path.exists()

    with np.load(target_path) as data:
        assert set(data.files) == {
            "ids",
            "category_keys",
            "display_names",
        }

        np.testing.assert_array_equal(
            data["ids"],
            np.array([1, 2], dtype=np.int64),
        )
        np.testing.assert_array_equal(
            data["category_keys"],
            np.array(["cat_a", "cat_b"], dtype="U100"),
        )
        np.testing.assert_array_equal(
            data["display_names"],
            np.array(["Kategorie A", "Kategorie B"], dtype="U100"),
        )

        assert data["ids"].dtype == np.dtype(np.int64)
        assert data["category_keys"].dtype == np.dtype("U100")
        assert data["display_names"].dtype == np.dtype("U100")

    captured = capsys.readouterr()
    assert captured.out == f"Created {target_path}\n"


def test_create_npz_file_from_empty_category_list(tmp_path):
    target_path = tmp_path / "empty_categories.npz"

    create_npz_file_from_category_list_json([], target_path)

    assert target_path.exists()

    with np.load(target_path) as data:
        assert data["ids"].shape == (0,)
        assert data["category_keys"].shape == (0,)
        assert data["display_names"].shape == (0,)

        assert data["ids"].dtype == np.dtype(np.int64)
        assert data["category_keys"].dtype == np.dtype("U100")
        assert data["display_names"].dtype == np.dtype("U100")


def test_create_npz_file_from_list_dataoverview(tmp_path, capsys):
    dataoverview = [
        SimpleNamespace(
            uuid="123e4567-e89b-12d3-a456-426614174000",
            umap_x=1.25,
            umap_y=2.5,
            umap_z=3.75,
            label="Label A",
            category="category_a",
            filename="file_a.wav",
            source="source_a",
            anomalie_isolation_forest=0.1,
            anomalie_LOF=0.2,
            anomalie_LOF_label="normal",
            anomalie_isolation_forest_label="anomaly",
            nearest_neighbors={
                "uuid-4": 0.53402,
                "uuid5": 0.66267,
            },
        ),
        SimpleNamespace(
            uuid="123e4567-e89b-12d3-a456-426614174001",
            umap_x=-1.0,
            umap_y=0.0,
            umap_z=5.5,
            label="Label B",
            category="category_b",
            filename="file_b.wav",
            source="source_b",
            anomalie_isolation_forest=-0.3,
            anomalie_LOF=1.5,
            anomalie_LOF_label="anomaly",
            anomalie_isolation_forest_label="normal",
            nearest_neighbors={
                "uuid-2": 0.53402,
                "uuid-3": 0.66267,
            },
        ),
    ]
    target_path = tmp_path / "dataoverview.npz"

    create_npz_file_from_list_DataOverview(dataoverview, target_path)

    assert target_path.exists()

    with np.load(target_path) as data:
        assert set(data.files) == {
            "uuids",
            "umap",
            "labels",
            "category_keys",
            "filenames",
            "sources",
            "anomalie_isolation_forest",
            "anomalie_lof",
            "anomalie_lof_labels",
            "anomalie_isolation_forest_labels",
            "nearest_neighbors",
        }

        np.testing.assert_array_equal(
            data["uuids"],
            np.array(
                [
                    "123e4567-e89b-12d3-a456-426614174000",
                    "123e4567-e89b-12d3-a456-426614174001",
                ],
                dtype="U36",
            ),
        )

        np.testing.assert_allclose(
            data["umap"],
            np.array(
                [
                    [1.25, 2.5, 3.75],
                    [-1.0, 0.0, 5.5],
                ],
                dtype=np.float64,
            ),
        )

        np.testing.assert_array_equal(
            data["labels"],
            np.array(["Label A", "Label B"], dtype="U100"),
        )
        np.testing.assert_array_equal(
            data["category_keys"],
            np.array(["category_a", "category_b"], dtype="U100"),
        )
        np.testing.assert_array_equal(
            data["filenames"],
            np.array(["file_a.wav", "file_b.wav"], dtype="U255"),
        )
        np.testing.assert_array_equal(
            data["sources"],
            np.array(["source_a", "source_b"], dtype="U100"),
        )

        np.testing.assert_allclose(
            data["anomalie_isolation_forest"],
            np.array([0.1, -0.3], dtype=np.float64),
        )
        np.testing.assert_allclose(
            data["anomalie_lof"],
            np.array([0.2, 1.5], dtype=np.float64),
        )

        np.testing.assert_array_equal(
            data["anomalie_lof_labels"],
            np.array(["normal", "anomaly"], dtype="U100"),
        )
        np.testing.assert_array_equal(
            data["anomalie_isolation_forest_labels"],
            np.array(["anomaly", "normal"], dtype="U100"),
        )
        np.testing.assert_array_equal(
            data["nearest_neighbors"],
            np.array(
                [
                    {
                        "uuid-4": 0.53402,
                        "uuid5": 0.66267,
                    },
                    {
                        "uuid-2": 0.53402,
                        "uuid-3": 0.66267,
                    },
                ],
                dtype="U1000",
            ),
        )

        assert data["umap"].shape == (2, 3)
        assert data["umap"].dtype == np.dtype(np.float64)
        assert data["filenames"].dtype == np.dtype("U255")
        assert data["nearest_neighbors"].dtype == np.dtype("U1000")

    captured = capsys.readouterr()
    assert captured.out == f"Created {target_path}\n"


def test_create_npz_file_from_empty_dataoverview_list(tmp_path):
    target_path = tmp_path / "empty_dataoverview.npz"

    create_npz_file_from_list_DataOverview([], target_path)

    assert target_path.exists()

    with np.load(target_path) as data:
        assert data["uuids"].shape == (0,)
        assert data["umap"].shape == (0,)
        assert data["labels"].shape == (0,)
        assert data["category_keys"].shape == (0,)
        assert data["filenames"].shape == (0,)
        assert data["sources"].shape == (0,)
        assert data["anomalie_isolation_forest"].shape == (0,)
        assert data["anomalie_lof"].shape == (0,)
        assert data["anomalie_lof_labels"].shape == (0,)
        assert data["anomalie_isolation_forest_labels"].shape == (0,)
        assert data["nearest_neighbors"].shape == (0,)


@pytest.mark.parametrize(
    ("function", "filename"),
    [
        (create_npz_file_from_category_list_json, "nested/categories.npz"),
        (create_npz_file_from_list_DataOverview, "nested/dataoverview.npz"),
    ],
)
def test_create_npz_file_fails_when_parent_directory_does_not_exist(
    tmp_path,
    function,
    filename,
):
    target_path = tmp_path / filename

    with pytest.raises(FileNotFoundError):
        function([], target_path)
