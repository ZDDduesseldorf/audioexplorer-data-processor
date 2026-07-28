from pathlib import Path

from app.processing.anomaly_detection.anomaly_service import AnomalyService
from app.processing.embeddings.embedding_service import (
    compute_embedding_from_list_ProcessedAudios,
)
from app.processing.nearest_neighbor_service import compute_nearest_neighbors
from app.processing.umap_service import calculate_umap_2d_from_list_embeddings
from app.processing.utils.json_utils import load_all_categories, write_json_file
from app.processing.utils.metadata_utils import load_all_metadata
from app.schemas.model import DataOverviewJSON
from app.services.npz_service import (
    create_npz_file_from_category_list_json,
    create_npz_file_from_list_DataOverview,
)
from app.services.run_audio_preprocessing import run_audio_preprocessing


def calculate_dataoverview_from_audio(
    path_audio_folder: Path,
    filename_metadata: str,
    target_path_audios: Path,
    target_filename_dataoverview: str,
):
    """Generate a DataOverview dataset from audio files.

    This function preprocesses audio files, computes embeddings, nearest
    neighbors, anomaly scores, and UMAP coordinates, combines the results
    with the corresponding metadata, and stores the resulting DataOverview
    objects as an NPZ file.

    The input directory can either contain audio files directly or multiple
    subdirectories, each with its own metadata file.

    Args:
        path_audio_folder: Directory containing audio files or subdirectories
            with audio files and metadata.
        filename_metadata: Name of the metadata file (e.g. ``metadata.json``).
        target_path_audios: Directory where processed audio files and the
            resulting DataOverview file will be stored.
        target_filename_dataoverview: Name of the output NPZ file.

    Raises:
        ValueError: If no audio files are found in the input directory.
    """

    all_audios = []
    all_metadata = {}

    subfolders = [p for p in path_audio_folder.iterdir() if p.is_dir()]

    if not subfolders:
        audios = run_audio_preprocessing(path_audio_folder, target_path_audios)
        if audios:
            all_audios.extend(audios)

        path_metadata = path_audio_folder / filename_metadata

        all_metadata.update(load_all_metadata(path_metadata))
    else:
        for folder in path_audio_folder.iterdir():
            if not folder.is_dir():
                continue

            metadata_path = folder / filename_metadata
            if not metadata_path.exists():
                print(f"Skipping {folder}: metadata.json missing")
                continue

            audios = run_audio_preprocessing(folder, target_path_audios)

            if audios is None:
                print(f"No audio files found in {folder}")
                continue

            all_audios.extend(audios)

            metadata = load_all_metadata(metadata_path)
            all_metadata.update(metadata)

    # laod and preprocess audio files

    if not all_audios:
        raise ValueError("No audio files found")
    # calculate Embeddings

    print("Calculate Embeddnings")
    embeddings = compute_embedding_from_list_ProcessedAudios(all_audios)

    print("Calculate nearest Neighbours")
    # calculate Nearest Neighbours
    nn_results = compute_nearest_neighbors(embeddings)

    print("Calculate Anomalies")
    # calculate Anomalies
    anomaly_service = AnomalyService()
    anomaly_results = anomaly_service.calculate_anomalies(embeddings)

    # calculate UMAP from embeddings

    print("Calculate UMAP")
    umap_results = calculate_umap_2d_from_list_embeddings(embeddings)

    # create DataOverview objects and save results as JSON
    list_DataOverview = create_DataOverview(
        all_metadata, umap_results, anomaly_results, nn_results
    )

    target_path_dataoverview = target_path_audios / target_filename_dataoverview
    create_npz_file_from_list_DataOverview(list_DataOverview, target_path_dataoverview)


def calculate_categories(target_folder_path, target_filename):
    """Generate and save the category overview.

    Loads all available categories and stores them as an NPZ file in the
    specified target directory.

    Args:
        target_folder_path: Directory where the category file should be saved.
        target_filename: Name of the output NPZ file.
    """
    list_categorys = load_all_categories()
    target_path_category = target_folder_path / target_filename
    target_folder_path.mkdir(parents=True, exist_ok=True)
    create_npz_file_from_category_list_json(list_categorys, target_path_category)


def save_results_as_json(
    list_DataOverview: list[DataOverviewJSON], target_json_path: Path
) -> None:
    """Save DataOverview objects as a JSON file.

    Converts a list of ``DataOverviewJSON`` objects into a dictionary keyed
    by UUID and writes the result to a JSON file.

    Args:
        list_DataOverview: List of DataOverview objects to serialize.
        target_json_path: Path to the output JSON file.
    """
    result = {}

    for item in list_DataOverview:
        result[item.uuid] = {
            "umap_x": item.umap_x,
            "umap_y": item.umap_y,
            "umap_z": item.umap_z,
            "label": item.label,
            "category": item.category,
            "original_filename": item.original_filename,
            "source": item.source,
            "additional_information": item.additional_information,
            "anomalie_isolation_forest": item.anomalie_isolation_forest,
            "anomalie_LOF": item.anomalie_LOF,
            "anomalie_isolation_forest_label": item.anomalie_isolation_forest_label,
            "anomalie_LOF_label": item.anomalie_LOF_label,
            "nearest_neighbors": item.nearest_neighbors,
        }

    write_json_file(target_json_path, result)


def create_DataOverview(
    metadata_results: dict,
    umap_results: dict,
    anomaly_results: dict,
    nn_results: dict,
) -> list[DataOverviewJSON]:
    """Create DataOverview objects from analysis results.

    Combines metadata, UMAP coordinates, anomaly detection results, and
    nearest-neighbor information into a list of ``DataOverviewJSON`` objects.
    Entries with missing metadata or analysis results are skipped.

    Args:
        metadata_results: Mapping of UUIDs to metadata dictionaries.
        umap_results: Mapping of UUIDs to computed UMAP coordinates.
        anomaly_results: Mapping of UUIDs to anomaly detection scores and
            labels.
        nn_results: Mapping of UUIDs to nearest-neighbor information.

    Returns:
        A list of populated ``DataOverviewJSON`` objects.
    """
    list_DataOverview = []

    for uuid, item in umap_results.items():
        metadata = metadata_results.get(uuid)

        if metadata is None:
            print(f"UUID is missing in metadata_results: {uuid}")
            continue

        anomaly = anomaly_results.get(uuid)

        if anomaly is None:
            print(f"UUID is missing in anomaly_results: {uuid}")
            continue

        neighbors = nn_results.get(uuid)

        if neighbors is None:
            print(f"UUID is missing in nn_results: {uuid}")
            continue

        additional_information = {}

        if metadata.get("context") is not None:
            additional_information["context"] = metadata["context"]

        if metadata.get("location") is not None:
            additional_information["location"] = metadata["location"]

        dataOverview_uuid = DataOverviewJSON(
            uuid=uuid,
            umap_x=item["umap_x"],
            umap_y=item["umap_y"],
            umap_z=item["umap_z"],
            label=metadata["label"],
            category=metadata["category"],
            original_filename=metadata["original_filename"],
            source=metadata["source"],
            additional_information=additional_information,
            anomalie_isolation_forest=anomaly["scores"]["isolation_forest"],
            anomalie_LOF=anomaly["scores"]["lof"],
            anomalie_isolation_forest_label=anomaly["labels"]["isolation_forest"],
            anomalie_LOF_label=anomaly["labels"]["lof"],
            nearest_neighbors=neighbors,
        )

        list_DataOverview.append(dataOverview_uuid)

    return list_DataOverview
