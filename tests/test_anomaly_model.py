import pytest
from src.anomaly_model import ZScoreDetector

def test_detector_flags_outlier():
    d = ZScoreDetector(window_size=5, threshold=2.0)
    sensor = 's1'
    values = [10, 11, 9, 10, 10]
    for v in values:
        is_anom, mean, std, z = d.update(sensor, v)
        assert not is_anom

    # feed an outlier
    is_anom, mean, std, z = d.update(sensor, 30)
    assert is_anom
