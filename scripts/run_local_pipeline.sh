#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

if [[ -d "venv" ]]; then
  echo "[INFO] Activating virtual environment."
  # shellcheck disable=SC1091
  source "venv/bin/activate"
fi

echo "[INFO] Starting Kafka weather producer..."
python -m src.ingest.kafka_producer_weather &
PRODUCER_PID=$!

cleanup() {
  echo "[INFO] Cleaning up background processes."
  if kill -0 "$PRODUCER_PID" >/dev/null 2>&1; then
    kill "$PRODUCER_PID"
  fi
}

trap cleanup EXIT

sleep 2
echo "[INFO] Running real-time pipeline..."
python -m src.processing.pipeline_runner
