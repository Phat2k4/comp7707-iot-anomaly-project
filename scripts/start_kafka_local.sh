#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Starting single-node Kafka stack via Docker..."

docker network inspect kafka-local >/dev/null 2>&1 || docker network create kafka-local

docker rm -f kafka-broker kafka-zookeeper >/dev/null 2>&1 || true

docker run -d --name kafka-zookeeper --network kafka-local \
  -p 2181:2181 \
  confluentinc/cp-zookeeper:7.5.0 \
  bash -c "ZOOKEEPER_CLIENT_PORT=2181 ZOOKEEPER_TICK_TIME=2000 /etc/confluent/docker/run"

docker run -d --name kafka-broker --network kafka-local \
  -p 9092:9092 \
  -e KAFKA_BROKER_ID=1 \
  -e KAFKA_ZOOKEEPER_CONNECT=kafka-zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  confluentinc/cp-kafka:7.5.0

cat <<'INSTRUCTIONS'

Kafka is booting up. Once ready you can create topics with:
  docker exec -it kafka-broker kafka-topics --create --topic weather_raw --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
  docker exec -it kafka-broker kafka-topics --create --topic weather_processed --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

Check broker logs:
  docker logs -f kafka-broker

Stop stack:
  docker rm -f kafka-broker kafka-zookeeper
INSTRUCTIONS
