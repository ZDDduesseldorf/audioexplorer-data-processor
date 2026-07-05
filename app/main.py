from app.services.pipeline import calculate_umap_from_audio
from app.config import (
    RAW_AUDIO_FOLDER,
    METADATA_FILEPATH,
    TARGET_AUDIO_FOLDER,
    TARGET_JSON_FILEPATH,
)


def run() -> str:
    return "Audioexplorer processing app is ready"


def main() -> None:

    print("Starting UMAP calculation from audio...")

    calculate_umap_from_audio(
        path_audio_folder=RAW_AUDIO_FOLDER,
        path_metadata=METADATA_FILEPATH,
        target_path_audios=TARGET_AUDIO_FOLDER,
        target_path_json=TARGET_JSON_FILEPATH,
    )

    print("UMAP calculation finished.")
    print(f"Processed audio files saved to: {TARGET_AUDIO_FOLDER}")
    print(f"Results saved to JSON file: {TARGET_JSON_FILEPATH}")

    print(run())


if __name__ == "__main__":
    main()
