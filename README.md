# COMP7707 – Real-time IoT Anomaly Detection

This repository contains our group project for COMP7707: a real-time IoT analytics pipeline built with Python, Kafka, and anomaly detection algorithms.

## Project Overview

The pipeline processes real-time IoT sensor data to detect anomalies in temperature, humidity, and other metrics. It supports both file-based simulation and live Kafka streaming.

## Folder Structure

```
comp7707-iot-anomaly-project/
│
├── src/                           # All production code
│   ├── ingest.py                  # Kafka consumer & data ingestion
│   ├── preprocess.py              # Data cleaning & normalization
│   ├── features.py                # Feature extraction & engineering
│   ├── anomaly_model.py           # Anomaly detection (z-score, etc.)
│   └── run_pipeline.py            # Main orchestration & CLI
│
├── notebooks/                     # Jupyter experiments & exploration
│   └── 01_explore_data.ipynb      # EDA, data analysis, visualization
│
├── config/                        # Configuration & examples
│   ├── config_example.yaml        # Pipeline configuration template
│   └── kafka_example.conf         # Kafka broker configuration
│
├── docs/                          # Reports, diagrams, documentation
│   └── ArchitectureDiagram.png    # System architecture diagram
│
├── data/                          # Sample data (non-sensitive)
│   └── sample_stream.csv          # Example IoT sensor records
│
├── tests/                         # Unit tests
│   └── test_anomaly_model.py      # Tests for anomaly detection
│
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Getting Started

### 1. Setup Python Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Pipeline (File-based Simulation)

```bash
python -m src.run_pipeline --source file --max 50
```

This reads from `data/sample_stream.csv` and processes up to 50 records, printing anomalies in real time.

### 3. Run Tests

```bash
pytest -q
```

Or with verbose output:

```bash
pytest -v
```

## Pipeline Stages

1. **Ingestion** (`ingest.py`): Reads IoT sensor data
   - Supports file-based and Kafka consumer modes
   - Fields: `timestamp`, `sensor_id`, `temp`, `humidity`

2. **Preprocessing** (`preprocess.py`): Cleans & normalizes data
   - Handles missing values
   - Type conversion & validation

3. **Feature Extraction** (`features.py`): Computes features
   - Rolling statistics (mean, std dev)
   - Trend analysis

4. **Anomaly Detection** (`anomaly_model.py`): Identifies outliers
   - Current: Z-score based detection (threshold: 3σ)
   - Marks points beyond 3 standard deviations as anomalies

## Sample Data Format

```csv
timestamp,sensor_id,temp,humidity
2025-11-15 10:00:00,sensor_A,21.5,40.2
2025-11-15 10:00:01,sensor_B,19.8,41.0
```

## Configuration

Edit `config/config_example.yaml` to customize:
- Anomaly thresholds
- Preprocessing parameters
- Output verbosity

## Development Workflow

1. **Experiment in notebooks**: Use `notebooks/01_explore_data.ipynb` for EDA
2. **Iterate in src/**: Develop functions and test with sample data
3. **Validate with tests**: Run unit tests to ensure correctness
4. **Deploy pipeline**: Run `run_pipeline.py` with actual data

## Notes

- **Kafka Integration**: `ingest.py` supports Kafka; requires a running broker and configuration in `config/`
- **Anomaly Detection**: Currently uses z-score per sensor; can be extended with ML models (Isolation Forest, LSTM, etc.)
- **Data Privacy**: `data/` contains only non-sensitive sample records for testing
- **Extensibility**: Add new preprocessing steps, features, or detection algorithms as needed

## Next Steps

- [ ] Improve anomaly detection with ML models
- [ ] Add real-time visualization dashboard
- [ ] Deploy with Docker containers
- [ ] Integrate with cloud storage (S3, etc.)