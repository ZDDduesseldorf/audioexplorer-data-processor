# Computes audio embeddings from raw waveforms using a loaded ModelManager.

import numpy as np
import torch

from app.processing.embeddings.model_manager import ModelManager
from app.services.preprocessing.config import AudioPreprocessingConfig
from app.schemas.model import PreprocessedAudio, EmbeddingData


def compute_embedding(waveform: np.ndarray, manager: ModelManager) -> np.ndarray:
    config = AudioPreprocessingConfig()

    inputs = manager.processor(
        audio=waveform,
        return_tensors="pt",
        sampling_rate=config.target_sample_rate,
    )

    with torch.no_grad():
        features = manager.model.get_audio_features(**inputs)

    features = features.pooler_output

    result: np.ndarray = features.cpu().numpy().squeeze(0)
    return result  # shape: (1, 512)


def compute_embeddings_batch(
    waveforms: list[np.ndarray], manager: ModelManager
) -> np.ndarray:
    embeddings = [compute_embedding(w, manager) for w in waveforms]
    return np.vstack(embeddings)  # shape: (N, 512)


def compute_embedding_from_list_ProcessedAudios(
    preprocessedAudio: list[PreprocessedAudio],
):

    manager = ModelManager()
    manager.load()

    list_embeddings = []

    for entry in preprocessedAudio:
        uuid = entry.uuid
        audio = entry.audio

        embedding = compute_embedding(audio, manager)

        embedding_calculated = EmbeddingData(uuid=uuid, embedding=embedding)

        list_embeddings.append(embedding_calculated)

    return list_embeddings
