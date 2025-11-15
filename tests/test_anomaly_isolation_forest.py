import pandas as pd
from sklearn.ensemble import IsolationForest

from src.models import anomaly_isolation_forest


def _sample_df():
    return pd.DataFrame(
        {
            "temp": [20.1, 21.5, 50.0],
            "humidity": [55, 57, 20],
            "pressure": [1013, 1014, 1000],
            "rolling_mean_temp": [20.1, 20.8, 30.0],
            "rolling_std_temp": [0.0, 0.7, 15.0],
            "rolling_mean_humidity": [55, 56, 40],
            "rolling_std_humidity": [0.0, 1.0, 10.0],
            "rolling_mean_pressure": [1013, 1014, 1007],
            "rolling_std_pressure": [0.0, 0.5, 5.0],
            "delta_temp": [0.0, 1.4, 28.5],
            "delta_humidity": [0.0, 2.0, -37.0],
            "delta_pressure": [0.0, 1.0, -14.0],
        }
    )


FEATURES = [
    "temp",
    "humidity",
    "pressure",
    "delta_temp",
    "delta_humidity",
    "delta_pressure",
    "rolling_mean_temp",
    "rolling_std_temp",
    "rolling_mean_humidity",
    "rolling_std_humidity",
    "rolling_mean_pressure",
    "rolling_std_pressure",
]


def test_train_initial_model_returns_isolation_forest():
    df = _sample_df()
    model = anomaly_isolation_forest.train_initial_model(df, FEATURES, contamination=0.5)
    assert isinstance(model, IsolationForest)


def test_predict_batch_appends_is_anomaly_column():
    df = _sample_df()
    model = anomaly_isolation_forest.train_initial_model(df, FEATURES, contamination=0.5)
    result = anomaly_isolation_forest.predict_batch(model, df, FEATURES)
    assert "is_anomaly" in result.columns
    assert set(result["is_anomaly"].unique()).issubset({0, 1})
