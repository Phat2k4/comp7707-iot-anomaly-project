"""Kafka producer that simulates weather sensor readings."""

from __future__ import annotations

import json
import random
import time
from datetime import datetime, timezone
from typing import Dict, List

from kafka import KafkaProducer

from src.utils.config_loader import load_config
from src.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)


def _simulate_sensor_payload(sensor_id: str) -> Dict[str, float]:
    """Create a pseudo-random reading for a single sensor."""

    base_temp = 22.0 + random.uniform(-5.0, 5.0)
    base_humidity = 55.0 + random.uniform(-10.0, 10.0)
    base_pressure = 1013.25 + random.uniform(-5.0, 5.0)

    return {
        "sensor_id": sensor_id,
        "temp": round(base_temp + random.uniform(-1.5, 1.5), 2),
        "humidity": round(base_humidity + random.uniform(-5.0, 5.0), 2),
        "pressure": round(base_pressure + random.uniform(-2.0, 2.0), 2),
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


def _init_producer(bootstrap_servers: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )


def run(config: Dict[str, Dict], frequency: int) -> None:
    kafka_cfg = config["kafka"]
    data_cfg = config["data"]
    producer = _init_producer(kafka_cfg["bootstrap_servers"])

    sensors: List[Dict[str, str]] = data_cfg.get("sensors", [])
    if not sensors:
        raise ValueError("No sensors configured in config[data][sensors].")

    topic = kafka_cfg["topic_raw"]
    LOGGER.info(
        "Starting weather producer to topic=%s with %d sensors at %ss interval",
        topic,
        len(sensors),
        frequency,
    )

    try:
        while True:
            for sensor in sensors:
                payload = _simulate_sensor_payload(sensor["id"])
                producer.send(topic, value=payload)
                LOGGER.info("Sent reading: %s", payload)
            producer.flush()
            time.sleep(max(1, frequency))
    except KeyboardInterrupt:
        LOGGER.info("Weather producer interrupted by user.")
    finally:
        producer.close()
        LOGGER.info("Kafka producer closed.")


def main() -> None:
    config = load_config()
    frequency = config.get("data", {}).get("frequency_seconds", 5)
    run(config, frequency)


if __name__ == "__main__":
    main()
