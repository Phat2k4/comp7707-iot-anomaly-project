"""Preprocessing helpers for IoT records."""
from typing import Dict, Optional
from datetime import datetime

def preprocess(record: Dict) -> Optional[Dict]:
    """Clean and normalize a single record.

    - Parse timestamp into ISO format (or keep as string if parsing fails)
    - Ensure numeric types for temp and humidity
    - Drop records missing both temp and humidity
    """
    if record is None:
        return None

    out = dict(record)
    ts = out.get("timestamp")
    if ts:
        try:
            # try common formats
            parsed = datetime.fromisoformat(ts)
            out["timestamp"] = parsed.isoformat()
        except Exception:
            try:
                parsed = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                out["timestamp"] = parsed.isoformat()
            except Exception:
                # leave as-is
                out["timestamp"] = ts

    try:
        out["temp"] = float(out.get("temp")) if out.get("temp") not in (None, "") else None
    except Exception:
        out["temp"] = None

    try:
        out["humidity"] = float(out.get("humidity")) if out.get("humidity") not in (None, "") else None
    except Exception:
        out["humidity"] = None

    if out.get("temp") is None and out.get("humidity") is None:
        return None

    return out
