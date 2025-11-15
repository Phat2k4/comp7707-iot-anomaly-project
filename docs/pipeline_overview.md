# Pipeline Overview

This COMP7707 project ingests simulated weather sensor data, processes it in real time, and flags potential anomalies.

## Stages
1. **Ingestion** – `src/ingest/kafka_producer_weather.py` simulates sensors and sends JSON payloads to Kafka (`topic_raw`). `kafka_consumer_raw.py` validates fields before downstream use.
2. **Preprocessing** – `src/processing/preprocess.py` converts dict payloads to pandas rows, handles missing values, and removes obvious outliers.
3. **Feature Extraction** – `src/processing/feature_extraction.py` maintains rolling statistics and rate-of-change metrics per sensor within streaming mini-batches.
4. **Modeling** – `src/models/anomaly_isolation_forest.py` hosts training/prediction utilities built on `sklearn` Isolation Forest. Predictions feed the dashboard and storage.
5. **Serving** – `src/dashboard/dashboard_streamlit.py` surfaces recent sensor trends and anomalies.

## Operational Notes
- Use `scripts/start_kafka_local.sh` to boot a local Kafka + ZooKeeper stack via Docker.
- Run the system end-to-end with `scripts/run_local_pipeline.sh`, which launches both the producer and pipeline runner.
- Generate sample historical data for notebooks and dashboard prototyping with `scripts/simulate_weather_data.py`.
