from app.config import (
    METADATA_FILENAME,
    RAW_AUDIO_FOLDER,
    TARGET_AUDIO_FOLDER,
    TARGET_FILENAME_CATEGORYS,
    TARGET_FILENAME_DATAOVERVIEW,
)
from app.services.api_import_service import import_categories, import_data_overview
from app.services.pipeline import (
    calculate_categories,
    calculate_dataoverview_from_audio,
)


def run() -> str:
    return "Audioexplorer processing app is ready"


def main() -> None:
    """Run the complete audio processing and import pipeline.

    This function executes the full workflow by:

    1. Generating the category NPZ file and importing it into the backend.
    2. Processing the audio dataset to compute embeddings, UMAP coordinates,
       anomaly scores, and nearest neighbors.
    3. Creating the DataOverview NPZ file and importing it into the backend.
    4. Printing a summary of the generated files and starting the application.

    The function assumes that all required input directories, metadata files,
    and configuration constants are available.
    """
    print("Create Category.npz")

    calculate_categories(
        target_folder_path=TARGET_AUDIO_FOLDER,
        target_filename=TARGET_FILENAME_CATEGORYS,
    )

    import_categories(TARGET_AUDIO_FOLDER / TARGET_FILENAME_CATEGORYS)

    print("Starting UMAP calculation from audio...")

    calculate_dataoverview_from_audio(
        path_audio_folder=RAW_AUDIO_FOLDER,
        filename_metadata=METADATA_FILENAME,
        target_path_audios=TARGET_AUDIO_FOLDER,
        target_filename_dataoverview=TARGET_FILENAME_DATAOVERVIEW,
    )

    import_data_overview(TARGET_AUDIO_FOLDER / TARGET_FILENAME_DATAOVERVIEW)

    print("UMAP calculation finished.")
    print(f"Processed audio files saved to: {TARGET_AUDIO_FOLDER}")
    print(
        f"Dataoverview saved to NPZ file: {TARGET_AUDIO_FOLDER} / {TARGET_FILENAME_DATAOVERVIEW}"
    )
    print(
        f"Categorys saved to NPZ file: {TARGET_AUDIO_FOLDER} / {TARGET_FILENAME_CATEGORYS}"
    )

    print(run())


if __name__ == "__main__":
    main()
