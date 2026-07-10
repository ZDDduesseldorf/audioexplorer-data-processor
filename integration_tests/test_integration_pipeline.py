from app.services.pipeline import calculate_umap_from_audio


from app.config import (
    RAW_AUDIO_FOLDER,
    METADATA_FILENAME,
    TARGET_AUDIO_FOLDER,
    TARGET_FILENAME_DATAOVERVIEW,
)


def test_run_pipeline():
    calculate_umap_from_audio(
        path_audio_folder=RAW_AUDIO_FOLDER,
        filename_metadata=METADATA_FILENAME,
        target_path_audios=TARGET_AUDIO_FOLDER,
        target_filename_dataoverview=TARGET_FILENAME_DATAOVERVIEW,
    )

    npz_path = TARGET_AUDIO_FOLDER / TARGET_FILENAME_DATAOVERVIEW
    assert npz_path.exists()
