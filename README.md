# **DATA-PROCESSOR**

# Overview

This repository is part of the audio-explorer project. More information about the overall project can be found in the backend repository:

https://github.com/ZDDduesseldorf/audioexplorer-backend

The data processor processes raw audio files and generates a data overview for each recording. The generated data is then imported into the backend database, During processing it:

- preprocesses the audio files,
- computes audio embeddings,
- calculates UMAP coordinates,
- determines nearest neighbours,
- performs anomaly detection, and
- generates metadata required for the data overview.

After processing, the categories and the data overview are imported into the backend database via the backend API.

## Running the Application with Docker

The data processor depends on the backend application. Therefore, make sure the backend is running before starting this application, as the processed data is imported directly into the backend database.

To build and start the application, run:

To start the application use:

```bash
git clone https://github.com/ZDDduesseldorf/audioexplorer-data-processor.git
docker compose up --build
```

## Default Directory Structure

By default, the application expects the following directory structure. All paths can be customized using environment variables (see the configuration section).

**Single dataset**

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

**Multiple datasets**

Subdirectories inside `raw_audios` are also supported.

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

After processing, the default output directory contains the processed audio files, data_overview.npz and category.npz:

```text
processed_audios/
├── uuid1.wav
├── uuid2.wav
├── uuid3.wav
|── category.npz
└── data_overview.npz
```

`processed_audios`: The processed_audios directory contains the preprocessed audio files used by the Audio Explorer.  
`data_overview.npz`: Contains the generated data for each audio file, including:

- UUID
- UMAP coordinates (x, y, z)
- Label
- Category
- Original filename
- Source
- Additional information
  - context
  - location
- Anomaly detection
  - Isolation Forest score
  - Isolation Forest label
  - Local Outlier Factor (LOF) score
  - LOF label
- Nearest neighbours
  - UUID
  - Distance

`category.npz`: Contains the available categories with the following fields:

- id
- key
- display_name

## Configuration

Default paths are defined in `config.py` and can be overridden using environment variables.

| Environment Variable           | Description                                                      | Default           |
| ------------------------------ | ---------------------------------------------------------------- | ----------------- |
| `AUDIOEXPLORER_DATA_DIR`       | Base data directory used to derive the default paths above.      | testdata          |
| `RAW_AUDIO_FOLDER`             | Path to the directory containing the raw audio files.            | raw_audios        |
| `METADATA_FILENAME`            | Name of the json-file that includes the metadata                 | metadata.json     |
| `TARGET_AUDIO_FOLDER`          | Target directory where the preprocessed audio files are written. | processed_audios  |
| `TARGET_FILENAME_DATAOVERVIEW` | Target filename of the generated data overview npz-file          | data_overview.npz |
| `TARGET_FILENAME_CATEGORYS`    | Target filename of the generated category npz-file               | category.npz      |

If only `AUDIOEXPLORER_DATA_DIR` is specified, all other paths are automatically derived from it using the default directory layout.

# Pipeline

The pipeline consists of all processing steps required to transform raw audio recordings into the final dataset used by the Audio Explorer.

The diagram below illustrates the complete processing pipeline, including the execution order of each step as well as the corresponding input and output formats.

![FlowChart pipeline process](img_readme/Audioexplorer-FlowChart.jpg)

Further details about each processing stage are provided in the following sections.

## Datasets

## Metadata

## Categories

## Audio Preprocessing

## Embedding calculation

## Nearest Neighbours

## UMAP

## Anomaly Detection
