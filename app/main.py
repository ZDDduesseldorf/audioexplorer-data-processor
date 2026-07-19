from app.services.pipeline import calculate_umap_from_audio
from app.config import (
    RAW_AUDIO_FOLDER,
    METADATA_FILENAME,
    TARGET_AUDIO_FOLDER,
    TARGET_FILENAME_CATEGORYS,
    TARGET_FILENAME_DATAOVERVIEW,
)

from app.processing.utils.json_utils import load_all_categories
from app.services.npz_service import create_npz_file_from_category_list_json
from app.services.api_import_service import import_categories, import_data_overview


def run() -> str:
    return "Audioexplorer processing app is ready"


def main() -> None:
    print("Create Category.npz")
    list_categorys = load_all_categories()
    target_path_category = TARGET_AUDIO_FOLDER / TARGET_FILENAME_CATEGORYS
    create_npz_file_from_category_list_json(list_categorys, target_path_category)
    import_categories(target_path_category)

    import_categories

    print("Starting UMAP calculation from audio...")

    calculate_umap_from_audio(
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
