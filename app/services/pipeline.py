from app.services.model import DataOverviewJSON
from app.services.json_utils import write_json_file
from app.services.metadata_utils import load_all_metadata
from scripts.run_audio_preprocessing import run_audio_preprocessing
from app.services.embedding_service import compute_embedding_from_list_ProcessedAudios
from app.services.umap_service import calculate_umap_2d_from_list_embeddings
from app.services.nearest_neighbor_service import compute_nearest_neighbors
from app.services.anomaly_detection.anomaly_service import AnomalyService
from pathlib import Path


def calculate_umap_from_audio(
    path_audio_folder: Path,
    path_metadata: Path,
    target_path_audios: Path,
    target_path_json: Path,
):
    """Calculate UMAP embeddings and anomaly scores from audio files and save the results as a JSON file."""
    # laod and preprocess audio files
    audios_preprocessed = run_audio_preprocessing(path_audio_folder, target_path_audios)

    # calculate Embeddings
    embeddings = compute_embedding_from_list_ProcessedAudios(audios_preprocessed)

    # calculate Nearest Neighbours
    nn_results = compute_nearest_neighbors(embeddings)

    # calculate Anomalies
    anomaly_service = AnomalyService()
    anomaly_results = anomaly_service.calculate_anomalies(embeddings)

    # calculate UMAP from embeddings

    umap_results = calculate_umap_2d_from_list_embeddings(embeddings)

    # load metadata and create DataOverview objects
    metadata_results = load_all_metadata(path_metadata)

    # create DataOverview objects and save results as JSON
    list_DataOverview = create_DataOverview(
        metadata_results, umap_results, anomaly_results, nn_results
    )

    save_results_as_json(list_DataOverview, target_path_json)


def save_results_as_json(
    list_DataOverview: list[DataOverviewJSON], target_json_path: Path
) -> None:
    """Save a list of DataOverviewJSON objects to a JSON file at the specified target path."""
    result = {}

    for item in list_DataOverview:
        result[item.uuid] = {
            "umap_x": item.umap_x,
            "umap_y": item.umap_y,
            "umap_z": item.umap_z,
            "label": item.label,
            "category": item.category,
            "filename": item.filename,
            "anomalie_isolation_forest": item.anomalie_isolation_forest,
            "anomalie_LOF": item.anomalie_LOF,
            "anomalie_isolation_forest_label": item.anomalie_isolation_forest_label,
            "anomalie_LOF_label": item.anomalie_LOF_label,
            "nearest_neighbors": item.nearest_neighbors,
        }

    write_json_file(target_json_path, result)


# TODO: def save_embeddings_as_json(embeddings):


def create_DataOverview(
    metadata_results: dict,
    umap_results: dict,
    anomaly_results: dict,
    nn_results: dict,
) -> list[DataOverviewJSON]:
    """Create a list of DataOverviewJSON objects from metadata, UMAP, anomaly and nearest neighbor results."""
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

        dataOverview_uuid = DataOverviewJSON(
            uuid=uuid,
            umap_x=item["umap_x"],
            umap_y=item["umap_y"],
            umap_z=item["umap_z"],
            label=metadata["label"],
            category=metadata["category"],
            filename=metadata["filename"],
            anomalie_isolation_forest=anomaly["scores"]["isolation_forest"],
            anomalie_LOF=anomaly["scores"]["lof"],
            anomalie_isolation_forest_label=anomaly["labels"]["isolation_forest"],
            anomalie_LOF_label=anomaly["labels"]["lof"],
            nearest_neighbors=neighbors,
        )

        list_DataOverview.append(dataOverview_uuid)

    return list_DataOverview
