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

        # If we have no history we cannot judge the new value yet. Store it and
        # return default statistics.
        if not dq:
            dq.append(value)
            return (False, value, 0.0, 0.0)

        # If we have not yet filled the window, treat the incoming value as part
        # of the warm-up period and do not attempt anomaly detection.
        if len(dq) < self.window_size:
            dq.append(value)
            mean = sum(dq) / len(dq)
            std = 0.0
            if len(dq) > 1:
                var = sum((x - mean) ** 2 for x in dq) / (len(dq) - 1)
                std = math.sqrt(var) if var > 0 else 0.0
            return (False, mean, std, 0.0)

        # Compute anomaly score using the existing history before we append the
        # new point. This prevents the candidate value from diluting its own
        # z-score by being included in the statistics we are comparing against.
        hist_mean = sum(dq) / len(dq)
        if len(dq) > 1:
            hist_var = sum((x - hist_mean) ** 2 for x in dq) / (len(dq) - 1)
            hist_std = math.sqrt(hist_var) if hist_var > 0 else 0.0
        else:
            hist_std = 0.0

        if hist_std > 0:
            z = (value - hist_mean) / hist_std
            is_anom = abs(z) >= self.threshold
        else:
            z = 0.0
            is_anom = False

        # Update the rolling window with the new observation and report the
        # refreshed statistics for visibility.
        dq.append(value)
        new_mean = sum(dq) / len(dq)
        if len(dq) > 1:
            new_var = sum((x - new_mean) ** 2 for x in dq) / (len(dq) - 1)
            new_std = math.sqrt(new_var) if new_var > 0 else 0.0
        else:
            new_std = 0.0

        return (is_anom, new_mean, new_std, z)
