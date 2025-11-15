# COMP7707 IoT Weather Anomaly Detection

Real-time anomaly detection pipeline for simulated weather sensors. Kafka carries events from a Python producer, preprocessing + feature extraction build streaming mini-batches, and an Isolation Forest model flags suspicious readings that the Streamlit dashboard highlights.

## Architecture Summary
- **Sensors / Producer** – `src/ingest/kafka_producer_weather.py` simulates multiple sensors and writes JSON payloads to Kafka (`topic_raw`).
- **Stream Processor** – `src/processing/pipeline_runner.py` consumes `topic_raw`, cleans the data, engineers rolling features, and runs the Isolation Forest model to produce anomaly labels. Detected anomalies can be re-published to `topic_processed`.
- **Storage + Dashboard** – anomalies are stored (placeholder: PostgreSQL / CSV). `src/dashboard/dashboard_streamlit.py` visualises time series, anomalies, and sensor trends.

Refer to `docs/ArchitectureDiagram.txt` and `docs/pipeline_overview.md` for more detail.

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
   Create the `weather_raw` and `weather_processed` topics using the commands echoed by the script.
3. **Generate sample data (optional)**
   ```bash
   python scripts/simulate_weather_data.py
   ```
4. **Run the streaming pipeline**
   ```bash
   ./scripts/run_local_pipeline.sh
   ```
   The script launches the Kafka producer in the background and runs the real-time pipeline runner.
5. **Launch the dashboard**
   ```bash
   streamlit run src/dashboard/dashboard_streamlit.py
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
