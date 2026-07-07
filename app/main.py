from app.services.pipeline import calculate_umap_from_audio
from app.config import (
    RAW_AUDIO_FOLDER,
    METADATA_FILENAME,
    TARGET_AUDIO_FOLDER,
    TARGET_JSON_FILENAME,
)


def run() -> str:
    return "Audioexplorer processing app is ready"


def main() -> None:

    print("Starting UMAP calculation from audio...")

    calculate_umap_from_audio(
        path_audio_folder=RAW_AUDIO_FOLDER,
        filename_metadata=METADATA_FILENAME,
        target_path_audios=TARGET_AUDIO_FOLDER,
        target_filename_json=TARGET_JSON_FILENAME,
    )

    print("UMAP calculation finished.")
    print(f"Processed audio files saved to: {TARGET_AUDIO_FOLDER}")
    print(f"Results saved to JSON file: {TARGET_AUDIO_FOLDER} / {TARGET_JSON_FILENAME}")

    print(run())


if __name__ == "__main__":
    main()
