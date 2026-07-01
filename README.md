# Running the Application with Docker

## Build the Docker Image

Build the image using:

```bash
docker build --build-arg AUDIOEXPLORER_DATA_DIR=data -t audioexplorer-data-processor:local .
```

The `AUDIOEXPLORER_DATA_DIR` build argument specifies the directory containing the input data that should be copied into the Docker image.

## Run the Container

To run the container with a mounted data directory:

```bash
docker run  -v "$(pwd)/data:/data" -e AUDIOEXPLORER_DATA_DIR=/data  audioexplorer-data-processor:local
```

The volume mount ensures that both the input data and all generated output files are stored on the host machine.

## Default Directory Structure

The application expects the following directory structure by default:

```text
app/
data/
├── raw_audios/
│   ├── metadata.json
│   ├── uuid1.wav
│   ├── uuid2.wav
│   └── uuid3.wav
└── processed_audios/
```

## Output Files

After processing, the default output directory contains:

```text
processed_audios/
├── uuid1.wav
├── uuid2.wav
├── uuid3.wav
└── data_overview.json
```

The `processed_audios` directory contains the preprocessed audio files, while `data_overview.json` contains the calculated UMAP coordinates, anomaly scores, nearest neighbors, and metadata for all processed audio files.

## Configuration

Default paths are defined in `config.py` and can be overridden using environment variables.

| Environment Variable                 | Description                                                      |
| ------------------------------------ | ---------------------------------------------------------------- |
| `AUDIOEXPLORER_RAW_AUDIO_FOLDER`     | Path to the directory containing the raw audio files.            |
| `AUDIOEXPLORER_METADATA_FILEPATH`    | Path to the `metadata.json` file.                                |
| `AUDIOEXPLORER_TARGET_AUDIO_FOLDER`  | Target directory where the preprocessed audio files are written. |
| `AUDIOEXPLORER_TARGET_JSON_FILEPATH` | Target path for the generated `data_overview.json` file.         |
| `AUDIOEXPLORER_DATA_DIR`             | Base data directory used to derive the default paths above.      |

If only `AUDIOEXPLORER_DATA_DIR` is specified, all other paths are automatically derived from it using the default directory layout.
