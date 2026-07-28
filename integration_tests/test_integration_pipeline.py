from app.config import (
    METADATA_FILENAME,
    RAW_AUDIO_FOLDER,
    TARGET_AUDIO_FOLDER,
    TARGET_FILENAME_CATEGORYS,
    TARGET_FILENAME_DATAOVERVIEW,
)
from app.services.pipeline import (
    calculate_categories,
    calculate_dataoverview_from_audio,
)


def test_run_pipeline_dataoverview():
    """Test that the DataOverview pipeline creates the expected NPZ file."""
    calculate_dataoverview_from_audio(
        path_audio_folder=RAW_AUDIO_FOLDER,
        filename_metadata=METADATA_FILENAME,
        target_path_audios=TARGET_AUDIO_FOLDER,
        target_filename_dataoverview=TARGET_FILENAME_DATAOVERVIEW,
    )

    npz_path = TARGET_AUDIO_FOLDER / TARGET_FILENAME_DATAOVERVIEW
    assert npz_path.exists()


def test_run_pipeline_categories():
    """Test that the category pipeline creates the expected NPZ file."""
    calculate_categories(TARGET_AUDIO_FOLDER, TARGET_FILENAME_CATEGORYS)

    npz_path = TARGET_AUDIO_FOLDER / TARGET_FILENAME_CATEGORYS
    assert npz_path.exists()
