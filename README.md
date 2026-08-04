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
The displayed and used audio files are supplied from five different sources. In the beginning of the project our group did receive a data set directly from the researchers of the Oxford University, which was later replaced for a updated version. To enchance the avaiable data we used four additional external data sets...

(Sharpen introduction and add number of audio files per source)

VocalSound:
Y. Gong, J. Yu and J. Glass, "Vocalsound: A Dataset for Improving Human Vocal Sounds Recognition," ICASSP 2022 - 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Singapore, Singapore, 2022, pp. 151-155, doi: 10.1109/ICASSP43922.2022.9746828.
keywords: {Training;Condition monitoring;Conferences;Buildings;Signal processing;Audio recording;Acoustics;vocal sounds;audio classification;corpus},

Deeply Inc.
@misc{deeply_nonverbal,
  title={{Deeply Nonverbal Vocalization dataset}},
  author={Deeply Inc.},
  year={2021},
  url={https://github.com/deeplyinc/Nonverbal-Vocalization-Dataset}
}

Nonspeech7k:
Muhammad Mamunur Rashid, Guiqing Li *, & Chengrui Du. (2023). Nonspeech7k dataset [Data set]. In IET Signal Processing (Version 1). Zenodo. https://doi.org/10.5281/zenodo.6967442

The Variably Intense Vocalizations of Affect and Emotion Corpus (VIVAE):
Holz, N., Larrouy-Maestri, P., & Poeppel, D. (2020). The Variably Intense Vocalizations of Affect and Emotion Corpus (VIVAE) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4066235

## Data Formatting



## Metadata
Metadata means data about data. It is structured information that describes, explains, or gives context to another piece of information or file, making it easier to find, use, and manage.
Case specific, it was used to provide every audio file with additional information in a uniform way that is readable for both humans and machines. As following... (picture for visual stimulation)

Pytaglib (libary python)

## Categories
Adopted as in nvv_clips june - only added "unknown"


## Labels
Didnt label yourself - to be defined for external category yes - Other for external category no

## Audio Preprocessing
### Overview
Audio preprocessing is the first step in the processing pipeline. It prepares raw audio files for further analysis by standardizing sample rates, filtering invalid audio files, reducing noise, and ensuring consistent audio quality. 

### Processing Steps
The preprocessing pipeline applies the following transformations to each audio file in sequence:

1. Mono Conversion & Resampling
<br>
Audio files are converted to mono and resampled to 48,000 Hz using Librosa resampling. This ensures compatibility with the CLAP embedding model that requires mono, 48 kHz input.

2. Length Filtering
<br>
Filters out audio files that do not meet duration requirements:
<br>
Minimum duration: 0.1 seconds <br>
Maximum duration: 30 seconds <br>
Audio files outside this range are excluded from further processing and logged as rejected samples.

3. Silence Filtering
<br>
Removes audio files that contain insufficient acoustic content by analyzing the Root Mean Square (RMS) energy. Files with RMS energy below the threshold of 0.005 are filtered out, as they typically contain only silence or very low-level noise.

4. Noise Reduction
<br>
Applies adaptive noise reduction to suppress background noise. A noise floor is estimated from quiet parts of the audio, and samples below this threshold are soft-suppressed based on the configured strength.

### Configuration

**Model Dependencies:**
The preprocessing parameters are optimized for the CLAP (Contrastive Language-Audio Pre-training) embedding model from Hugging Face (laion/larger_clap_general). If using a different embedding model, adjust these parameters accordingly.

Default preprocessing parameters can be modified via environment variables or by editing `audio_config.py`:

| Parameter | Default | Description |
| --- | --- | --- |
| `target_sample_rate` | 48,000 Hz | Target sample rate for resampling - must match model requirements |
| `apply_length_filter` | true | Enable/disable duration filtering |
| `min_duration_seconds` | 0.1 | Minimum audio duration in seconds |
| `max_duration_seconds` | 30.0 | Maximum audio duration in seconds |
| `apply_silence_filter` | true | Enable/disable silence filtering |
| `silence_rms_threshold` | 0.005 | RMS energy threshold for silence detection |
| `apply_noise_reduction` | true | Enable/disable noise reduction |
| `noise_reduction_strength` | 1.0 | Strength factor for noise reduction (0-1) |


### Input & Output

**Input**: Raw audio files in various formats (WAV, MP3, FLAC, etc.) with different sample rates, typically sourced from `raw_audios/` directory with accompanying `metadata.json`.

**Output**: Preprocessed mono audio files saved to `processed_audios/` directory in WAV format at 48 kHz. Only audio files that pass all filtering criteria are output.

### Impementation Details
The audio preprocessing is implemented in `app/processing/audio/`:

- `audio_config.py` - Configuration parameters
- `resampler.py` - Sample rate conversion using Librosa
- `filter.py` - Duration, silence, and noise reduction filters
- `loader.py` - Audio file loading
- `saver.py` - Preprocessed audio file saving

## Embedding calculation

## Nearest Neighbours

## UMAP

## Anomaly Detection

The anomaly detection module identifies unusual audio samples based on their embedding vectors.

The complete workflow is coordinated by the `AnomalyService`, which executes two complementary anomaly detection algorithms, combines their results, assigns human-readable labels, and returns a structured output dictionary.

---

The anomaly detection pipeline utilizes two unsupervised machine learning algorithms provided by the **scikit-learn** library: **Isolation Forest** and **Local Outlier Factor (LOF)**.

Both detectors validate the input embeddings, compute anomaly scores, normalize the scores, and return structured results for further analysis and visualization.

---

The algorithms return raw anomaly scores rather than percentages. These raw values are relative model outputs and differ between Isolation Forest and LOF. To provide a consistent and interpretable representation, the scores are inverted where necessary and normalized to a shared range between **0 and 100** using Min-Max normalization.

The resulting percentage expresses the relative anomaly strength within the analyzed dataset. Finally, each normalized anomaly score is rounded to two decimal places before being added to the result dictionary.

### Isolation Forest

The Isolation Forest implementation is based on:

```python
from sklearn.ensemble import IsolationForest
```

Isolation Forest detects **global anomalies** by recursively partitioning the embedding space using randomly generated decision trees. Samples that require fewer partitions to become isolated receive higher anomaly scores.

### Local Outlier Factor (LOF)

The Local Outlier Factor implementation is based on:

```python
from sklearn.neighbors import LocalOutlierFactor
```

Local Outlier Factor (LOF) detects **local anomalies** by comparing the local density around each embedding with the density of its nearest neighbors. Embeddings located in significantly lower-density regions than their surrounding neighborhood receive higher anomaly scores.

### Score Normalization

Since the two algorithms produce scores on different numerical scales, all raw anomaly scores are normalized to a common range between **0 and 100** using Min-Max normalization. This enables a direct comparison between the outputs of both algorithms.

### Label Assignment

Normalized anomaly scores are converted into the following human-readable categories using the `AnomalyLabeler`:

- Not Anomalous
- Slightly Anomalous
- Anomalous
- Highly Anomalous

### Output

The anomaly detection service returns one result entry for each embedding.

```json
{
    "uuid1": {
        "scores": {
            "isolation_forest": 58.03,
            "lof": 88.04
        },
        "labels": {
            "isolation_forest": "Anomalous",
            "lof": "Highly Anomalous"
        }
    }
}
```

The returned dictionary contains the normalized anomaly scores and their corresponding labels for both Isolation Forest and Local Outlier Factor, indexed by the embedding UUID.
