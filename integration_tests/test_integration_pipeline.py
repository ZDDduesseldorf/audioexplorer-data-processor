from app.services.pipeline import (
    calculate_dataoverview_from_audio,
    calculate_categories,
)


from app.config import (
    RAW_AUDIO_FOLDER,
    METADATA_FILENAME,
    TARGET_AUDIO_FOLDER,
    TARGET_FILENAME_DATAOVERVIEW,
    TARGET_FILENAME_CATEGORYS,
)


def test_run_pipeline_dataoverview():
    calculate_dataoverview_from_audio(
        path_audio_folder=RAW_AUDIO_FOLDER,
        filename_metadata=METADATA_FILENAME,
        target_path_audios=TARGET_AUDIO_FOLDER,
        target_filename_dataoverview=TARGET_FILENAME_DATAOVERVIEW,
    )

    npz_path = TARGET_AUDIO_FOLDER / TARGET_FILENAME_DATAOVERVIEW
    assert npz_path.exists()


def test_run_pipeline_categories():
    calculate_categories(TARGET_AUDIO_FOLDER, TARGET_FILENAME_CATEGORYS)

    npz_path = TARGET_AUDIO_FOLDER / TARGET_FILENAME_CATEGORYS
    assert npz_path.exists()
