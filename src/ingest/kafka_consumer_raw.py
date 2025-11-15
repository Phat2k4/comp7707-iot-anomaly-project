"""Kafka consumer for raw weather sensor events."""

from __future__ import annotations

import json
from typing import Dict, Generator

from kafka import KafkaConsumer

from src.utils.config_loader import load_config
from src.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)
REQUIRED_FIELDS = {"sensor_id", "temp", "humidity", "pressure", "timestamp"}


def _init_consumer(config: Dict) -> KafkaConsumer:
    kafka_cfg = config["kafka"]
    consumer = KafkaConsumer(
        kafka_cfg["topic_raw"],
        bootstrap_servers=kafka_cfg["bootstrap_servers"],
        group_id=kafka_cfg["group_id"],
        value_deserializer=lambda val: json.loads(val.decode("utf-8")),
        auto_offset_reset="latest",
        enable_auto_commit=True,
    )
    return consumer


def _validate_payload(payload: Dict) -> bool:
    missing = REQUIRED_FIELDS.difference(payload.keys())
    if missing:
        LOGGER.warning("Dropping payload missing fields %s: %s", missing, payload)
        return False
    return True


def consume_raw_stream(
    config_path: str = "config/config_example.yaml",
) -> Generator[Dict, None, None]:
    """Yield validated payloads from the raw Kafka topic."""

    config = load_config(config_path)
    consumer = _init_consumer(config)
    LOGGER.info("Consuming from topic=%s", config["kafka"]["topic_raw"])

    try:
        for message in consumer:
            payload = message.value
            if _validate_payload(payload):
                yield payload
    finally:
        LOGGER.info("Shutting down raw consumer.")
        consumer.close()


def _main() -> None:
    for event in consume_raw_stream():
        LOGGER.info("Received event: %s", event)


if __name__ == "__main__":
    _main()
