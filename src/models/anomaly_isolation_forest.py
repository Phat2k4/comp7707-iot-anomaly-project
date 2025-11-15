"""Isolation Forest utilities for anomaly detection."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


def train_initial_model(
    df_train: pd.DataFrame,
    feature_cols: Iterable[str],
    contamination: float = 0.02,
    random_state: int = 42,
) -> IsolationForest:
    """Fit an IsolationForest model."""

    model = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_estimators=200,
        n_jobs=-1,
    )
    model.fit(df_train[list(feature_cols)])
    return model


def predict_batch(
    model: IsolationForest, df_batch: pd.DataFrame, feature_cols: Iterable[str]
) -> pd.DataFrame:
    """Return dataframe annotated with anomaly predictions."""

    if model is None:
        raise ValueError("Model must be trained before predicting.")

    df = df_batch.copy()
    predictions = model.predict(df[list(feature_cols)])
    df["is_anomaly"] = (predictions == -1).astype(int)
    return df


def save_model(model: IsolationForest, path: Path) -> Path:
    """Persist model to disk."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return path


def load_model(path: Path) -> Optional[IsolationForest]:
    """Load a persisted model if it exists."""

    path = Path(path)
    if not path.exists():
        return None
    return joblib.load(path)
