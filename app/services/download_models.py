# Downloads the necessary models to the local cache.
# Run this once to pre-warm the cache before serving requests.

import logging
import sys

sys.path.insert(0, ".")

from app.processing.embeddings.model_manager import ModelManager

logging.basicConfig(level=logging.INFO)


def main() -> None:
    manager = ModelManager()
    manager.load()
    print("CLAP model downloaded and cached.")


if __name__ == "__main__":
    main()
