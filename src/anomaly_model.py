"""Simple streaming anomaly detector using z-score per sensor."""
from collections import deque, defaultdict
from typing import Dict, Tuple
import math

class ZScoreDetector:
    """Maintain a rolling window of recent values per sensor and flag anomalies."""
    def __init__(self, window_size: int = 30, threshold: float = 3.0):
        self.window_size = window_size
        self.threshold = threshold
        self.data = defaultdict(lambda: deque(maxlen=self.window_size))

    def update(self, sensor_id: str, value: float) -> Tuple[bool, float, float, float]:
        """Update window for sensor and return (is_anomaly, mean, std, zscore).

        If not enough data (less than 2 points), returns (False, mean, std, 0.0)
        """
        dq = self.data[sensor_id]
        dq.append(value)
        if len(dq) < 2:
            mean = sum(dq) / len(dq)
            return (False, mean, 0.0, 0.0)

        mean = sum(dq) / len(dq)
        var = sum((x - mean) ** 2 for x in dq) / (len(dq) - 0)
        std = math.sqrt(var) if var >= 0 else 0.0
        z = (value - mean) / std if std > 0 else 0.0
        is_anom = abs(z) >= self.threshold
        return (is_anom, mean, std, z)
