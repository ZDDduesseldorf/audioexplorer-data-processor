from app.services.pipeline import calculate_umap_from_audio


from app.config import (
    RAW_AUDIO_FOLDER,
    METADATA_FILENAME,
    TARGET_AUDIO_FOLDER,
    TARGET_JSON_FILENAME,
)


def test_run_pipeline():
    calculate_umap_from_audio(
        path_audio_folder=RAW_AUDIO_FOLDER,
        filename_metadata=METADATA_FILENAME,
        target_path_audios=TARGET_AUDIO_FOLDER,
        target_filename_json=TARGET_JSON_FILENAME,
    )

    npz_path = TARGET_AUDIO_FOLDER / "dataoverview.npz"
    assert npz_path.exists()
