# COMP7707 IoT Weather Anomaly Detection

This repository hosts our COMP7707 group project: a real-time IoT weather analytics pipeline that streams simulated sensor data through Kafka, cleans and enriches it with Python, detects anomalies using Isolation Forest, and visualises results with Streamlit.

## Architecture Summary
- **Sensors / Producer** – `src/ingest/kafka_producer_weather.py` simulates multiple sensors and publishes JSON payloads to the Kafka `topic_raw`.
- **Stream Processor** – `src/processing/pipeline_runner.py` consumes `topic_raw`, applies preprocessing (`preprocess.py`) and feature engineering (`feature_extraction.py`), then scores anomalies with `src/models/anomaly_isolation_forest.py`. Detected events can be republished to `topic_processed`.
- **Storage & Dashboard** – anomalies are stored (PostgreSQL placeholder or CSV) and surfaced via `src/dashboard/dashboard_streamlit.py`.

For a textual walkthrough see `docs/ArchitectureDiagram.txt` and `docs/pipeline_overview.md`.

## Getting Started
1. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Start Kafka locally**
   ```bash
   ./scripts/start_kafka_local.sh
   ```
   Create the `weather_raw` and `weather_processed` topics using the commands printed by the script.
3. **(Optional) Generate sample data**
   ```bash
   python scripts/simulate_weather_data.py
   ```
4. **Run the real-time pipeline**
   ```bash
   ./scripts/run_local_pipeline.sh
   ```
   This launches the Kafka weather producer in the background and starts the streaming pipeline.
5. **Launch the dashboard**
   ```bash
   streamlit run src/dashboard/dashboard_streamlit.py
   ```
6. **Run unit tests**
   ```bash
   pytest
   ```

## Folder Structure
```
comp7707-iot-weather/
├── src/
│   ├── ingest/
│   │   ├── kafka_producer_weather.py
│   │   └── kafka_consumer_raw.py
│   ├── processing/
│   │   ├── preprocess.py
│   │   ├── feature_extraction.py
│   │   └── pipeline_runner.py
│   ├── models/
│   │   ├── anomaly_isolation_forest.py
│   │   └── model_utils.py
│   ├── dashboard/
│   │   └── dashboard_streamlit.py
│   └── utils/
│       ├── config_loader.py
│       └── logging_utils.py
├── config/
│   ├── config_example.yaml
│   └── kafka_example.conf
├── scripts/
│   ├── start_kafka_local.sh
│   ├── run_local_pipeline.sh
│   └── simulate_weather_data.py
├── notebooks/01_offline_exploration.ipynb
├── docs/
│   ├── ArchitectureDiagram.txt
│   └── pipeline_overview.md
├── data/sample_weather_data.csv
├── tests/test_anomaly_isolation_forest.py
├── requirements.txt
└── README.md
```

## Pipeline Stages
1. **Ingestion (`src/ingest/`)**
   - `kafka_producer_weather.py` loads config via PyYAML, simulates sensor metrics, and streams JSON to Kafka at the configured cadence.
   - `kafka_consumer_raw.py` validates each payload (required fields, JSON parsing) and yields records for downstream processing.
2. **Preprocessing (`src/processing/preprocess.py`)**
   - Cleans raw dicts, coerces numeric values, drops/marks out-of-range readings (e.g., temp outside [-40, 60]) as NaN, converts to pandas DataFrame, and interpolates missing data.
3. **Feature Extraction (`src/processing/feature_extraction.py`)**
   - Adds rolling mean/std features plus rate-of-change metrics (delta temperature, humidity, pressure) per sensor within mini-batches.
4. **Modeling (`src/models/anomaly_isolation_forest.py`)**
   - Provides `train_initial_model`, `predict_batch`, and joblib save/load helpers for the Isolation Forest detector.
   - `model_utils.py` contains config helpers, train/validation splits, and evaluation utilities (precision/recall/F1) for labeled datasets.
5. **Pipeline Runner (`src/processing/pipeline_runner.py`)**
   - Accumulates batches (default 100 records), applies preprocessing & feature extraction, trains an initial model if needed, scores anomalies, logs them, and (placeholder) republishes to `topic_processed`.
6. **Dashboard (`src/dashboard/dashboard_streamlit.py`)**
   - Reads from PostgreSQL/CSV (sample file by default), renders time-series charts with highlighted anomalies, and exposes controls for sensor selection/time window.

## Sample Data & Configuration
- `scripts/simulate_weather_data.py` creates `data/sample_weather_data.csv` covering three sensors over 24 hours with injected anomalies.
- `config/config_example.yaml` defines Kafka endpoints, sensor metadata, model hyperparameters, and storage DSN placeholders.
- `config/kafka_example.conf` documents common Kafka broker settings for local setups.

## Notes & Next Steps
- Extend `_publish_processed` in `pipeline_runner.py` to push anomalies to Kafka `topic_processed` or write them into PostgreSQL.
- Containerise the services (Kafka, producer, pipeline, dashboard) for reproducible deployments.
- Swap the simulated sensors with real weather hardware feeds as they become available, and retrain the Isolation Forest with historical data for better accuracy.
