"""Streamlit dashboard for monitoring weather anomalies."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path("data/sample_weather_data.csv")


@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    """Load sensor data from CSV or fallback to simulated data."""

    if path.exists():
        df = pd.read_csv(path)
    else:
        st.warning(f"{path} not found. Generating synthetic data for demo purposes.")
        timestamps = pd.date_range(end=pd.Timestamp.utcnow(), periods=500, freq="min")
        sensors = ["sensor_north_01", "sensor_central_02", "sensor_south_03"]
        df = pd.DataFrame(
            {
                "timestamp": np.random.choice(timestamps, size=500),
                "sensor_id": np.random.choice(sensors, size=500),
                "temp": np.random.normal(22, 4, size=500),
                "humidity": np.random.normal(55, 8, size=500),
                "pressure": np.random.normal(1013, 5, size=500),
            }
        )

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if "is_anomaly" not in df.columns:
        df["is_anomaly"] = ((df["temp"] > 35) | (df["temp"] < 0)).astype(int)
    return df.sort_values("timestamp")


def filter_data(df: pd.DataFrame, sensor_id: str, hours: int) -> pd.DataFrame:
    cutoff = df["timestamp"].max() - pd.Timedelta(hours=hours)
    return df[(df["sensor_id"] == sensor_id) & (df["timestamp"] >= cutoff)]


def render_chart(df: pd.DataFrame, field: str) -> None:
    fig = px.line(df, x="timestamp", y=field, title=f"{field.title()} over Time")
    anomalies = df[df["is_anomaly"] == 1]
    if not anomalies.empty:
        fig.add_scatter(
            x=anomalies["timestamp"],
            y=anomalies[field],
            mode="markers",
            marker=dict(color="red", size=10, symbol="x"),
            name="Anomaly",
        )
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.set_page_config(
        page_title="IoT Weather Anomaly Dashboard",
        layout="wide",
    )
    st.title("Real-time IoT Weather Anomaly Dashboard")
    st.caption("COMP7707 – Streamed via Kafka, processed with Python.")

    data = load_data(DATA_PATH)
    sensor_id = st.sidebar.selectbox("Sensor", sorted(data["sensor_id"].unique()))
    window = st.sidebar.slider("Time window (hours)", 1, 24, value=6)

    filtered = filter_data(data, sensor_id, window)
    st.subheader(f"Sensor {sensor_id} | last {window} hours")

    col1, col2 = st.columns(2)
    with col1:
        render_chart(filtered, "temp")
    with col2:
        render_chart(filtered, "humidity")

    st.markdown("### Recent Observations")
    st.dataframe(
        filtered.sort_values("timestamp", ascending=False)[
            ["timestamp", "sensor_id", "temp", "humidity", "pressure", "is_anomaly"]
        ].head(50),
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
