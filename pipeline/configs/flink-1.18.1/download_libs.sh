#!/bin/bash

mkdir -p ./lib

curl -o ./lib/flink-connector-jdbc-3.1.2-1.18.jar https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.2-1.18/flink-connector-jdbc-3.1.2-1.18.jar
curl -o ./lib/clickhouse-jdbc-0.3.2.jar https://repo1.maven.org/maven2/ru/yandex/clickhouse/clickhouse-jdbc/0.3.2/clickhouse-jdbc-0.3.2.jar
curl -o ./lib/flink-sql-connector-kafka-3.1.0-1.18.jar https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.1.0-1.18/flink-sql-connector-kafka-3.1.0-1.18.jar
# curl -o ./lib/clickhouse-jdbc.jar https://github.com/ClickHouse/clickhouse-java/releases/clickhouse-jdbc-0.7.0.jar
# curl -o ./lib/flink-connector-kafka-3.2.0-1.18.jar https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka/3.2.0-1.18/flink-connector-kafka-3.2.0-1.18.jar

echo "Libs downloaded successfully"