from pathlib import Path

import pandas as pd


def load_metadata_as_df(path: Path) -> pd.DataFrame:
    """Load metadata into a pandas DataFrame.

    Reads the metadata JSON file at the specified path and returns its
    contents as a pandas DataFrame.

    Args:
        path: Path to the metadata JSON file.

    Returns:
        A DataFrame containing the metadata.
    """
    metadata = pd.read_json(path)

    return metadata


def load_all_metadata(path_metadata: Path) -> dict:
    """Load all metadata as a dictionary.

    Reads the metadata JSON file and converts each entry into a dictionary
    keyed by the corresponding UUID. Optional fields such as ``context`` and
    ``location`` are set to ``None`` if no value is available.

    Args:
        path_metadata: Path to the metadata JSON file.

    Returns:
        A dictionary mapping UUIDs to their corresponding metadata.
    """
    df = load_metadata_as_df(path_metadata)

    metadata = {}

    for _, row in df.iterrows():
        metadata[row.uuid] = {
            "label": row.label,
            "category": row.category,
            "original_filename": row.filename,
            "source": row.source,
            "context": None if pd.isna(row.get("context")) else row.get("context"),
            "location": None if pd.isna(row.get("location")) else row.get("location"),
        }

    return metadata
