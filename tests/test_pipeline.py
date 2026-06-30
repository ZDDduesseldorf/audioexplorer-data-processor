import pytest
import json
import scripts.pipeline as pipe
from app.services.model import DataOverviewJSON


@pytest.fixture
def sample_metadata_results():
    return {
        "1": {
            "label": "laughing",
            "category": "laugh",
            "filename": "1.wav",
        },
        "2": {
            "label": "crying",
            "category": "cry",
            "filename": "2.wav",
        },
    }


@pytest.fixture
def sample_umap_results():
    return {
        "1": {
            "umap_x": 0.1,
            "umap_y": 0.2,
            "umap_z": 0.3,
        },
        "2": {
            "umap_x": 0.4,
            "umap_y": 0.5,
            "umap_z": 0.6,
        },
    }


@pytest.fixture
def sample_anomaly_results():
    return {
        "1": {
            "scores": {
                "isolation_forest": -0.1,
                "lof": 1.2,
            },
            "labels": {
                "isolation_forest": "normal",
                "lof": "normal",
            },
        },
        "2": {
            "scores": {
                "isolation_forest": -0.8,
                "lof": 2.7,
            },
            "labels": {
                "isolation_forest": "anomaly",
                "lof": "anomaly",
            },
        },
    }


@pytest.fixture
def sample_nn_results():
    return {
        "1": {"2": 0.083},
        "2": {"1": 0.043},
    }


def test_create_DataOverview(
    sample_metadata_results,
    sample_umap_results,
    sample_anomaly_results,
    sample_nn_results,
):
    # TODO: anomaly ergänzen
    response = pipe.create_DataOverview(
        sample_metadata_results,
        sample_umap_results,
        sample_anomaly_results,
        sample_nn_results,
    )

    assert len(response) == 2
    assert response[0].uuid == "1"
    assert response[0].label == "laughing"
    assert response[0].umap_x == 0.1
    assert response[0].anomalie_LOF == 1.2
    assert response[0].nearest_neighbors == {"2": 0.083}


def test_create_data_overview_skips_missing_nn(
    sample_metadata_results, sample_umap_results, sample_anomaly_results
):
    nn_results = {}

    result = pipe.create_DataOverview(
        sample_metadata_results, sample_umap_results, sample_anomaly_results, nn_results
    )

    assert result == []


def test_create_data_overview_skips_missing_metadata(
    sample_umap_results, sample_anomaly_results, sample_nn_results
):
    metadata_results = {}

    result = pipe.create_DataOverview(
        metadata_results, sample_umap_results, sample_anomaly_results, sample_nn_results
    )

    assert result == []


def test_save_results_as_json(tmp_path):
    data_overview = [
        DataOverviewJSON(
            uuid="uuid_1",
            umap_x=1.0,
            umap_y=2.0,
            umap_z=3.0,
            label="laughing",
            category="laugh",
            filename="uuid_1.wav",
            anomalie_isolation_forest=0.0,
            anomalie_LOF=0.0,
            anomalie_isolation_forest_label="unknown",
            anomalie_LOF_label="unknown",
            nearest_neighbors={"uuid_2": 0.083},
        )
    ]

    output_file = tmp_path / "data_overview.json"

    pipe.save_results_as_json(data_overview, output_file)

    saved = json.loads(output_file.read_text(encoding="utf-8"))

    assert "uuid_1" in saved
    assert saved["uuid_1"]["umap_x"] == 1.0
    assert saved["uuid_1"]["label"] == "laughing"
    assert saved["uuid_1"]["nearest_neighbors"] == {"uuid_2": 0.083}
    assert "uuid" not in saved["uuid_1"]
