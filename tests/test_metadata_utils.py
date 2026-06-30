import app.processing.utils.metadata_utils as meta
from app.config import get_data_file_path
import pandas as pd
import pytest


@pytest.fixture
def test_metadata():
    metadata_path = get_data_file_path("metadata.json")
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
        "sample-001": {
            "label": "laughing",
            "category": "to be defined",
            "filename": "a_RA1_01_01__xh6fC2ZfwU_moan.wav",
        },
        "2": {
            "label": "laughing",
            "category": "to be defined",
            "filename": "a_RA2_056_XSoJqdPi4Iw_groaning.wav",
        },
        "3": {
            "label": "laughing",
            "category": "to be defined",
            "filename": "a_RA2_093_FL1LUiqNITo_oohsound.wav",
        },
    }
