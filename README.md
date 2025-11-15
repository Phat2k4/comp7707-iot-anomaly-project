# COMP7707 – Real-time IoT Anomaly Detection

This repository contains our group project for COMP7707: a real-time IoT analytics pipeline built with Python.

## Structure
- `src/`: ingestion, preprocessing, feature extraction, anomaly detection
- `notebooks/`: data exploration & experiments
- `docs/`: architecture diagram, report assets
- `config/`: example configuration files
- `data/`: sample (non-sensitive) data
- `tests/`: unit tests

## How to run (local simulation)

1. Create a Python environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the pipeline (file-based simulation):

```bash
python -m src.run_pipeline --source file --max 50
```

3. To run tests:

```bash
pytest -q
```

## Notes
- `src/ingest.py` supports a Kafka consumer if you provide a running Kafka cluster and the `kafka-python` package.
- The current anomaly detector is a simple z-score per sensor; improve later with feature rich models.
# comp7707-iot-anomaly-project