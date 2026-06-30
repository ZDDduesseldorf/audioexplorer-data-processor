# Manages loading and in-memory caching of the model we use (at the moment CLAP from Hugging Face).

import logging

from transformers import ClapModel, ClapProcessor

CLAP_MODEL_ID: str = "laion/larger_clap_general"
CLAP_MODEL_REVISION: str = "ada0c23a36c4e8582805bb38fec3905903f18b41"

_log = logging.getLogger(__name__)


class ModelManager:
    def __init__(self, model_id: str = CLAP_MODEL_ID) -> None:
        self._model_id = model_id
        self._model: ClapModel | None = None
        self._processor: ClapProcessor | None = None

    def load(self) -> None:
        if self._model is not None:
            return
        _log.info("Loading CLAP model: %s", self._model_id)
        self._processor = ClapProcessor.from_pretrained(
            self._model_id, revision=CLAP_MODEL_REVISION
        )
        self._model = ClapModel.from_pretrained(
            self._model_id, revision=CLAP_MODEL_REVISION
        )
        self._model.eval()
        _log.info("CLAP model ready.")

    @property
    def model(self) -> ClapModel:
        if self._model is None:
            raise RuntimeError("Call load() before accessing the model.")
        return self._model

    @property
    def processor(self) -> ClapProcessor:
        if self._processor is None:
            raise RuntimeError("Call load() before accessing the processor.")
        return self._processor

    @property
    def is_loaded(self) -> bool:
        return self._model is not None
