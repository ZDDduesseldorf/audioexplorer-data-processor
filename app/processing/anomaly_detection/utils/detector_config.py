class DetectorConfig:
    # -----------------------------------
    # ISOLATION FOREST
    # -----------------------------------

    ISOLATION_FOREST = {
        # Controls how difficult it is for a data point to be classified as an anomaly.
        # Represents the expected proportion of anomalies in the dataset.
        # Currently assumes that approximately 3% of samples are anomalous.
        "contamination": 0.03,
        # Number of decision trees used in the Isolation Forest ensemble.
        # More trees generally improve stability but increase computation time.
        "n_estimators": 100,
        # Random seed used to ensure reproducible results across runs.
        # Using the same seed produces the same random behavior every time.
        "random_state": 42,
    }

    # -----------------------------------
    # LOCAL OUTLIER FACTOR
    # -----------------------------------

    LOF = {
        # Controls how difficult it is for a data point to be classified as an anomaly.
        # Has the same meaning as the contamination parameter in Isolation Forest.
        # Currently assumes that approximately 7% of samples are anomalous.
        "contamination": 0.07,
        # Number of neighboring points considered when estimating local density.
        # LOF compares each point to its 20 nearest neighbors.
        "n_neighbors": 20,
        # Distance metric used to measure similarity between data points.
        # For audio embeddings, this measures how similar or different
        # two audio samples are in the embedding space.
        # LOF identifies anomalies as points with significantly lower
        # local density than their surrounding neighbors.
        "metric": "euclidean",
    }
