"""Orchestrates the streaming anomaly detection pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from src.ingest.kafka_consumer_raw import consume_raw_stream
from src.models import anomaly_isolation_forest
from src.processing import feature_extraction, preprocess
from src.utils.config_loader import load_config
from src.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)
MODEL_ARTIFACT = Path("models/isolation_forest.joblib")


def run_realtime_pipeline(
    config_path: str = "config/config_example.yaml", batch_size: int = 100
) -> None:
    """Run the end-to-end streaming pipeline."""

    config = load_config(config_path)
    feature_cols = feature_extraction.default_feature_columns()
    model = _load_or_init_model(feature_cols)

    buffer: List[dict] = []

    for payload in consume_raw_stream(config_path):
        record = preprocess.clean_record(payload)
        if record is None:
            continue
        buffer.append(record)

        if len(buffer) < batch_size:
            continue

        df = preprocess.records_to_dataframe(buffer)
        df = preprocess.handle_missing(df)
        if df.empty:
            buffer.clear()
            continue

        df = feature_extraction.add_features(df)
        df = _ensure_feature_columns(df, feature_cols)

        if model is None:
            LOGGER.info("Training initial model on first batch.")
            model = anomaly_isolation_forest.train_initial_model(df, feature_cols)
            anomaly_isolation_forest.save_model(model, MODEL_ARTIFACT)

        result_df = anomaly_isolation_forest.predict_batch(model, df, feature_cols)
        anomalies = result_df[result_df["is_anomaly"] == 1]
        if not anomalies.empty:
            LOGGER.warning("Detected %d anomalies", len(anomalies))
            LOGGER.warning("%s", anomalies[["sensor_id", "timestamp", "temp", "is_anomaly"]])
            _publish_processed(anomalies, config)

        buffer.clear()


def _ensure_feature_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            df[column] = 0.0
    return df


def _load_or_init_model(feature_cols: List[str]):
    if MODEL_ARTIFACT.exists():
        LOGGER.info("Loading model artifact from %s", MODEL_ARTIFACT)
        return anomaly_isolation_forest.load_model(MODEL_ARTIFACT)
    LOGGER.info("Model artifact not found. Will train when enough data accumulates.")
    return None


def _publish_processed(anomalies: pd.DataFrame, config: dict) -> None:
    """Placeholder for publishing anomalies to Kafka or another sink."""

    topic = config["kafka"]["topic_processed"]
    LOGGER.info("Publish %d anomalies to topic=%s (implementation TBD)", len(anomalies), topic)


if __name__ == "__main__":
    run_realtime_pipeline()
