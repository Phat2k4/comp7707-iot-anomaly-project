"""Glue to run the streaming pipeline locally (file-based simulation by default)."""
from src.ingest import consume_stream
from src.preprocess import preprocess
from src.features import extract_features
from src.anomaly_model import ZScoreDetector
import argparse

def main(source: str = "file", max_records: int = 0):
    detector = ZScoreDetector(window_size=30, threshold=3.0)
    stream = consume_stream(source=source)
    count = 0
    for rec in stream:
        pre = preprocess(rec)
        if pre is None:
            continue
        feat = extract_features(pre)
        sid = feat.get("sensor_id")
        temp = feat.get("temp")
        if sid is None or temp is None:
            continue
        is_anom, mean, std, z = detector.update(sid, temp)
        if is_anom:
            print(f"ANOMALY sensor={sid} time={feat.get('timestamp')} temp={temp} z={z:.2f} mean={mean:.2f} std={std:.2f}")
        else:
            print(f"OK sensor={sid} temp={temp} z={z:.2f}")
        count += 1
        if max_records and count >= max_records:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="file", help="Source: 'file' or 'kafka'")
    parser.add_argument("--max", type=int, default=0, help="Max records to process (0 = unlimited)")
    args = parser.parse_args()
    main(source=args.source, max_records=args.max)
