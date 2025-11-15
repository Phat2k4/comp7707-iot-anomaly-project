"""Helper utilities for working with anomaly detection models."""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import train_test_split

from src.utils.config_loader import load_config


def load_project_config(path: str = "config/config_example.yaml") -> Dict:
    """Wrapper around utils.load_config for convenience."""

    return load_config(path)


def split_train_validation(
    df: pd.DataFrame, validation_fraction: float = 0.2, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split historical data for offline experimentation."""

    train_df, val_df = train_test_split(
        df, test_size=validation_fraction, shuffle=True, random_state=random_state
    )
    return train_df, val_df


def evaluate_model(
    model,
    df: pd.DataFrame,
    feature_cols: Iterable[str],
    label_col: str,
) -> Dict[str, float]:
    """Compute precision / recall / F1 using labeled anomaly data."""

    if label_col not in df.columns:
        raise ValueError(f"Label column {label_col} not present in dataframe.")

    predictions = model.predict(df[list(feature_cols)])
    y_pred = (predictions == -1).astype(int)
    y_true = df[label_col].astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )
    return {"precision": precision, "recall": recall, "f1": f1}
