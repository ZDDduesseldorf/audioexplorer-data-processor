import app.processing.utils.metadata_utils as meta
from app.config import get_data_file_path
import pandas as pd
import pytest


@pytest.fixture
def test_metadata():
    metadata_path = get_data_file_path("raw_audios/metadata.json")
    return metadata_path


def test_load_metadata_as_df(tmp_path):
    file = tmp_path / "meta.json"

    expected = pd.DataFrame(
        {
            "uuid": ["uuid_1"],
            "filename": ["a.wav"],
            "label": ["laughing"],
            "category": ["laugh"],
            "source": ["folder"],
        }
    )

    expected.to_json(file)

    result = meta.load_metadata_as_df(file)

    assert len(result) == 1
    assert list(result.columns) == list(expected.columns)
    assert result.iloc[0]["uuid"] == "uuid_1"


def test_load_all_metadata(test_metadata):
    metadata = meta.load_all_metadata(test_metadata)

    assert len(metadata) == 3
    assert metadata == {
        "0a0b8b81-6e0f-4a35-90cf-4cca0e4d3007": {
            "label": "laughing",
            "category": "laugh",
            "filename": "a_RA1_01_01__xh6fC2ZfwU_moan.wav",
            "source": "nvv_clips",
        },
        "0a0b8b81-6e0f-4a35-90cf-4cca0e4d3006": {
            "label": "crying",
            "category": "cry",
            "filename": "a_RA2_056_XSoJqdPi4Iw_groaning.wav",
            "source": "nvv_clips",
        },
        "0a0b8b81-6e0f-4a35-90cf-4cca0e4d3005": {
            "label": "screaming",
            "category": "scream",
            "filename": "a_RA2_093_FL1LUiqNITo_oohsound.wav",
            "source": "nvv_clips",
        },
    }
