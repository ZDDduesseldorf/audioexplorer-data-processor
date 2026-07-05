import pandas as pd
from pathlib import Path


def load_metadata_as_df(path: Path) -> pd.DataFrame:
    """Load metadata from a JSON file at the given path and return it as a pandas DataFrame."""
    metadata = pd.read_json(path)

    return metadata


def load_all_metadata(path_metadata: Path) -> dict:
    """Load all metadata from a JSON file at the given path and return it as a dictionary."""
    df = load_metadata_as_df(path_metadata)

    metadata = {}

    for _, row in df.iterrows():
        metadata[row.uuid] = {
            "label": row.label,
            "category": row.category,
            "filename": row.filename,
        }

    return metadata
