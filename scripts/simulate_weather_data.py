"""Generate sample weather data for local experimentation."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/sample_weather_data.csv")
SENSORS = ["sensor_north_01", "sensor_central_02", "sensor_south_03"]


def generate_records() -> pd.DataFrame:
    end = pd.Timestamp.utcnow().floor("min")
    start = end - timedelta(hours=24)
    timestamps = pd.date_range(start=start, end=end, freq="min", inclusive="left")

    rows: List[dict] = []
    for sensor in SENSORS:
        sensor_offset = SENSORS.index(sensor) * 1.5
        temp_wave = np.sin(np.linspace(0, 3.14 * 4, len(timestamps))) * 5
        humidity_wave = np.cos(np.linspace(0, 3.14 * 2, len(timestamps))) * 5
        for idx, ts in enumerate(timestamps):
            temp = 20 + sensor_offset + temp_wave[idx] + np.random.normal(0, 0.8)
            humidity = 55 + humidity_wave[idx] + np.random.normal(0, 2)
            pressure = 1013 + np.random.normal(0, 1.5)
            rows.append(
                {
                    "timestamp": ts,
                    "sensor_id": sensor,
                    "temp": round(temp, 2),
                    "humidity": round(humidity, 2),
                    "pressure": round(pressure, 2),
                    "is_anomaly": 0,
                }
            )

    df = pd.DataFrame(rows)
    anomaly_indices = np.random.choice(df.index, size=12, replace=False)
    df.loc[anomaly_indices, "temp"] += np.random.choice([15, -15], size=len(anomaly_indices))
    df.loc[anomaly_indices, "is_anomaly"] = 1
    return df


def main() -> None:
    df = generate_records()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(df)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
