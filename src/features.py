"""Feature extraction for streaming IoT records."""
from typing import Dict

def extract_features(record: Dict) -> Dict:
    """Add derived features to a record and return new dict.

    Current simple features:
    - temp_humidity_ratio: temp / humidity when humidity > 0
    """
    out = dict(record)
    temp = out.get("temp")
    hum = out.get("humidity")
    if temp is not None and hum:
        try:
            out["temp_humidity_ratio"] = temp / hum
        except Exception:
            out["temp_humidity_ratio"] = None
    else:
        out["temp_humidity_ratio"] = None

    return out
