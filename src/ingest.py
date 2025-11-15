"""Ingestion utilities for COMP7707 IoT pipeline.

Provides `consume_stream()` which yields cleaned records as dicts.

Behavior:
- If `source=='kafka'` attempts to use `kafka.KafkaConsumer` (requires `kafka-python`).
- Otherwise reads from `data/sample_stream.csv` and yields rows.
"""
from typing import Dict, Generator, Optional
import csv
import time

def _parse_row(row: Dict[str, str]) -> Optional[Dict]:
    try:
        return {
            "timestamp": row.get("timestamp"),
            "sensor_id": row.get("sensor_id"),
            "temp": float(row.get("temp")) if row.get("temp") not in (None, "") else None,
            "humidity": float(row.get("humidity")) if row.get("humidity") not in (None, "") else None,
        }
    except Exception:
        return None

def consume_stream(source: str = "file", file_path: str = "data/sample_stream.csv",
                   kafka_topic: Optional[str] = None, bootstrap_servers: str = "localhost:9092",
                   poll_interval: float = 0.1) -> Generator[Dict, None, None]:
    """Yield cleaned records as dicts from the chosen source.

    Example record fields: timestamp, sensor_id, temp, humidity

    If `source=='kafka'` a simple Kafka consumer is attempted. Otherwise the function
    falls back to reading `file_path` in a loop (simulating a stream).
    """
    if source == "kafka":
        try:
            from kafka import KafkaConsumer
            import json

            consumer = KafkaConsumer(
                kafka_topic,
                bootstrap_servers=bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
            )
            for msg in consumer:
                r = msg.value
                parsed = _parse_row(r)
                if parsed:
                    yield parsed
        except Exception:
            # If kafka is not available, fall back to file
            pass

    # File-based fallback: stream rows from CSV repeatedly
    while True:
        try:
            with open(file_path, "r", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    parsed = _parse_row(row)
                    if parsed:
                        yield parsed
                        time.sleep(poll_interval)
        except FileNotFoundError:
            # No sample data yet — sleep and retry
            time.sleep(1)
