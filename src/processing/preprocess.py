"""Preprocessing utilities for incoming weather events."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional

import pandas as pd

TEMP_RANGE = (-40.0, 60.0)
HUMIDITY_RANGE = (0.0, 100.0)
PRESSURE_RANGE = (900.0, 1100.0)
NUMERIC_FIELDS = ("temp", "humidity", "pressure")


def clean_record(record: Dict) -> Optional[Dict]:
    """
    Normalise an individual record and coerce obvious outliers to NaN.

    Returns None if the record is missing required keys.
    """

    if not all(field in record for field in ("sensor_id", "timestamp", *NUMERIC_FIELDS)):
        return None

    cleaned = dict(record)
    for field in NUMERIC_FIELDS:
        try:
            cleaned[field] = float(cleaned[field])
        except (TypeError, ValueError):
            cleaned[field] = float("nan")

    cleaned["temp"] = _clamp_to_range(cleaned["temp"], TEMP_RANGE)
    cleaned["humidity"] = _clamp_to_range(cleaned["humidity"], HUMIDITY_RANGE)
    cleaned["pressure"] = _clamp_to_range(cleaned["pressure"], PRESSURE_RANGE)

    return cleaned


def records_to_dataframe(records: Iterable[Dict]) -> pd.DataFrame:
    """Convert cleaned dicts into a pandas DataFrame."""

    df = pd.DataFrame(list(records))
    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Interpolate missing numeric values and drop rows still containing NaNs."""

    if df.empty:
        return df

    df_sorted = df.sort_values("timestamp")
    df_sorted[NUMERIC_FIELDS] = (
        df_sorted[NUMERIC_FIELDS].interpolate(method="linear", limit_direction="both")
    )
    return df_sorted.dropna(subset=NUMERIC_FIELDS)


def _clamp_to_range(value: float, allowed: tuple) -> float:
    if value != value:  # NaN check
        return value
    lower, upper = allowed
    if lower <= value <= upper:
        return value
    return float("nan")
