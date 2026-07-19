from pydantic import BaseModel, ConfigDict

import numpy as np


class PreprocessedAudio(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    uuid: str
    audio: np.ndarray


class EmbeddingData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    uuid: str
    embedding: np.ndarray


class DataOverviewJSON(BaseModel):
    uuid: str
    umap_x: float
    umap_y: float
    umap_z: float
    label: str
    category: str
    original_filename: str
    source: str
    additional_information: dict[str, str | None] | None = None
    anomalie_isolation_forest: float
    anomalie_LOF: float
    anomalie_isolation_forest_label: str
    anomalie_LOF_label: str
    nearest_neighbors: dict[str, float]


class CategoryListItem(BaseModel):
    id: int
    key: str
    name: str
