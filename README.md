# Running the Application with Docker

This application processes the raw audio data and its metadata to generate a data overview. The categories are also read from a JSON file. The data overview and the categories are saved as NPZ files. They are also imported directly into the database of the associated Git repository (https://github.com/ZDDduesseldorf/audioexplorer-backend/tree/main). For this to work, the repository’s Docker container must also be running.

```bash
docker compose up --build
```

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
├── processed_audios/
└── category_list.json
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
├── processed_audios/
└── category_list.json

```

## Output Files

After processing, the default output directory contains:

```text
processed_audios/
├── uuid1.wav
├── uuid2.wav
├── uuid3.wav
|── category.npz
└── data_overview.npz
```

The `processed_audios` directory contains the preprocessed audio files, while `data_overview.json` contains the calculated UMAP coordinates, anomaly scores, nearest neighbors, and metadata for all processed audio files.

## Configuration

Default paths are defined in `config.py` and can be overridden using environment variables.

| Environment Variable           | Description                                                      | Default           |
| ------------------------------ | ---------------------------------------------------------------- | ----------------- |
| `RAW_AUDIO_FOLDER`             | Path to the directory containing the raw audio files.            | raw_audios        |
| `METADATA_FILENAME`            | Name of the json-file that includes the metadata                 | metadata.json     |
| `TARGET_AUDIO_FOLDER`          | Target directory where the preprocessed audio files are written. | processed_audios  |
| `TARGET_FILENAME_DATAOVERVIEW` | Target filename of the generated data overview npz-file          | data_overview.npz |
| `TARGET_FILENAME_CATEGORYS`    | Target filename of the generated category npz-file               | category.npz      |
| `AUDIOEXPLORER_DATA_DIR`       | Base data directory used to derive the default paths above.      | testdata          |

If only `AUDIOEXPLORER_DATA_DIR` is specified, all other paths are automatically derived from it using the default directory layout.
