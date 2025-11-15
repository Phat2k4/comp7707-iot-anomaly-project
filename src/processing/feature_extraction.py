"""Feature engineering for streaming mini-batches."""

from __future__ import annotations

from typing import List

import pandas as pd

ROLLING_WINDOW = 5


def add_features(df_batch: pd.DataFrame, window: int = ROLLING_WINDOW) -> pd.DataFrame:
    """Augment the batch with rolling statistics and deltas."""

    if df_batch.empty:
        return df_batch

    df = df_batch.sort_values("timestamp").copy()
    grouped = df.groupby("sensor_id")
    numeric_fields = ["temp", "humidity", "pressure"]

    for field in numeric_fields:
        df[f"rolling_mean_{field}"] = grouped[field].transform(
            lambda series: series.rolling(window, min_periods=1).mean()
        )
        df[f"rolling_std_{field}"] = grouped[field].transform(
            lambda series: series.rolling(window, min_periods=1).std().fillna(0.0)
        )

    df["delta_temp"] = grouped["temp"].diff().fillna(0.0)
    df["delta_humidity"] = grouped["humidity"].diff().fillna(0.0)
    df["delta_pressure"] = grouped["pressure"].diff().fillna(0.0)

    return df


def default_feature_columns() -> List[str]:
    """Return the list of engineered feature columns used by the model."""

    core = ["temp", "humidity", "pressure", "delta_temp", "delta_humidity", "delta_pressure"]
    rolling = [
        "rolling_mean_temp",
        "rolling_std_temp",
        "rolling_mean_humidity",
        "rolling_std_humidity",
        "rolling_mean_pressure",
        "rolling_std_pressure",
    ]
    return core + rolling
