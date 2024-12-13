from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import JdbcSink
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import MapFunction

from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer,
    KafkaSource,
)
from dotenv import load_dotenv
import os
# Tải biến môi trường từ .env
load_dotenv()

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_HEAD_TOPIC = os.getenv("KAFKA_HEAD_TOPIC")

# Lấy các biến môi trường
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "clickhouse")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "default")

class SampleRecordGenerator(MapFunction):
    def map(self, value):
        return (1, "Sample Review", 5, "2023-10-01", 123, 456)

def initialize_env() -> StreamExecutionEnvironment:
    """Khởi tạo môi trường thực thi Flink"""
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # Điều chỉnh theo nhu cầu

    # Lấy đường dẫn hiện tại của script
    root_dir_list = __file__.split("/")[:-1]  # Sửa lại nếu thư mục khác
    root_dir = "/".join(root_dir_list)
    print(f"Root directory: {root_dir}")

    # Thêm ClickHouse JDBC driver vào classpath
    jar_path = f"file://{root_dir}/lib/clickhouse-jdbc-0.3.2.jar"
    print(f"Adding JAR: {jar_path}")
    env.add_jars(jar_path)
    return env

def main():
    # Khởi tạo môi trường Flink
    env = initialize_env()
    print("🟢 Flink environment initialized")

    # Tạo DataStream với sample records
    data_stream = env.from_elements(1).map(SampleRecordGenerator(), output_type=Types.TUPLE([
        Types.INT(),     # review_id
        Types.STRING(),  # review_content
        Types.INT(),     # review_rating
        Types.STRING(),  # review_date
        Types.INT(),     # customer_id_id
        Types.INT()      # product_id_id
    ]))

    # Định nghĩa JDBC sink
    jdbc_sink = JdbcSink.sink(
        "INSERT INTO reviews (review_id, review_content, review_rating, review_date, customer_id_id, product_id_id) VALUES (?, ?, ?, ?, ?, ?)",
        lambda stmt, record: [
            stmt.set_int(1, record[0]),
            stmt.set_string(2, record[1]),
            stmt.set_int(3, record[2]),
            stmt.set_string(4, record[3]),
            stmt.set_int(5, record[4]),
            stmt.set_int(6, record[5])
        ],
        Types.TUPLE([
            Types.INT(),     # review_id
            Types.STRING(),  # review_content
            Types.INT(),     # review_rating
            Types.STRING(),  # review_date
            Types.INT(),     # customer_id_id
            Types.INT()      # product_id_id
        ]),
        "jdbc:clickhouse://clickhouse:8123/default",
        "default",
        "default"
    )

    # Thêm sink vào DataStream
    data_stream.add_sink(jdbc_sink)
    print("🟢 Sink added to DataStream")

    # Thực thi Flink job
    env.execute("InsertSampleRecordToClickHouse")

if __name__ == "__main__":
    main()