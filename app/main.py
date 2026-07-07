from app.services.pipeline import calculate_umap_from_audio
from app.config import (
    RAW_AUDIO_FOLDER,
    METADATA_FILENAME,
    TARGET_AUDIO_FOLDER,
    TARGET_JSON_FILENAME,
)

from app.processing.utils.json_utils import load_all_categories
from app.services.npz_service import create_npz_file_from_category_list_json
from app.services.api_import_service import import_categories, import_data_overview


def run() -> str:
    return "Audioexplorer processing app is ready"


def main() -> None:

    print("Starting UMAP calculation from audio...")

    list_categorys = load_all_categories()
    target = TARGET_AUDIO_FOLDER / "category.npz"
    create_npz_file_from_category_list_json(list_categorys, target)
    import_categories(target)

    import_categories

    calculate_umap_from_audio(
        path_audio_folder=RAW_AUDIO_FOLDER,
        filename_metadata=METADATA_FILENAME,
        target_path_audios=TARGET_AUDIO_FOLDER,
        target_filename_json=TARGET_JSON_FILENAME,
    )

    import_data_overview(TARGET_AUDIO_FOLDER / "dataoverview.npz")

    print("UMAP calculation finished.")
    print(f"Processed audio files saved to: {TARGET_AUDIO_FOLDER}")
    print(f"Results saved to JSON file: {TARGET_AUDIO_FOLDER} / {TARGET_JSON_FILENAME}")

    print(run())


if __name__ == "__main__":
    main()
