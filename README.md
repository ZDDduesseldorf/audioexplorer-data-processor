# Running the Application with Docker

```bash
docker compose up
```

The `AUDIOEXPLORER_DATA_DIR` build argument specifies the directory containing the input data that should be copied into the Docker image.

## Default Directory Structure

The application expects the following directory structure by default, when runnig with docker compose up:

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

or it also takes subfolders

```text
app/
data/
├── raw_audios/
|   ├── folder1/
│       ├── metadata.json
│       ├── uuid1.wav
│       ├── uuid2.wav
│       └── uuid3.wav
|   ├── folder2/
│       ├── metadata.json
│       ├── uuid4.wav
│       ├── uuid5.wav
│       └── uuid6.wav
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

| Environment Variable     | Description                                                      | Default            |
| ------------------------ | ---------------------------------------------------------------- | ------------------ |
| `RAW_AUDIO_FOLDER`       | Path to the directory containing the raw audio files.            | raw_audios         |
| `METADATA_FILENAME`      | Name of the json-file that includes the metadata                 | metadata.json      |
| `TARGET_AUDIO_FOLDER`    | Target directory where the preprocessed audio files are written. | processed_audios   |
| `TARGET_JSON_FILENAME`   | Target filename of the generated data                            | data_overview.json |
| `AUDIOEXPLORER_DATA_DIR` | Base data directory used to derive the default paths above.      | testdata           |

If only `AUDIOEXPLORER_DATA_DIR` is specified, all other paths are automatically derived from it using the default directory layout.
