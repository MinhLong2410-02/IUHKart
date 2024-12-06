import json, os
import logging
import clickhouse_connect
from datetime import datetime

from pyflink.common import Types, WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer,
    KafkaSource,
)

from dotenv import load_dotenv
load_dotenv()
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_HEAD_TOPIC = os.getenv("KAFKA_HEAD_TOPIC")

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def initialize_env() -> StreamExecutionEnvironment:
    """Makes stream execution environment initialization"""
    env = StreamExecutionEnvironment.get_execution_environment()

    # Get current directory
    root_dir_list = __file__.split("/")[:-2]
    root_dir = "/".join(root_dir_list)

    # Adding the jar to the flink streaming environment
    env.add_jars(
        f"file://{root_dir}/lib/flink-sql-connector-kafka-3.1.0-1.18.jar",
    )
    return env

def configure_source(server:str, topic:str,  earliest:bool = False) -> KafkaSource:
    """Makes kafka source initialization"""
    properties = {
        "bootstrap.servers": server,
        "group.id": "warehouse",
    }

    offset = KafkaOffsetsInitializer.latest()
    if earliest:
        offset = KafkaOffsetsInitializer.earliest()

    kafka_source = (
        KafkaSource.builder()
        .set_topics(topic)
        .set_properties(properties)
        .set_starting_offsets(offset)
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    return kafka_source

def process_debezium_message(message: str):
    """Phân tích thông điệp Debezium và trích xuất thông tin thay đổi."""
    try:
        message_json = json.loads(message)
        payload = message_json.get('payload', {})
        operation = payload.get('op')
        before = payload.get('before')
        after = payload.get('after')

        if operation == 'c':
            action = "Create"
            data = after
        elif operation == 'u':
            action = "Update"
            data = after
        elif operation == 'd':
            action = "Delete"
            data = before
        else:
            action = "Unknown"
            data = {}

        logger.info(f"🟢 Action: {action}")
        return operation, data

    except json.JSONDecodeError as e:
        logger.error(f"🔻 Lỗi khi giải mã JSON: {e}")
    except Exception as e:
        logger.error(f"❌ Đã xảy ra lỗi: {e}")

def get_clickhouse_client():
    """Initialize ClickHouse client."""
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
    )
    return client

def stream_customer(message: str, client):
    """Process and sink data into ClickHouse."""
    attributes = ['id', 'first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'signup_date']
    try:
        # Parse the Kafka message
        mode, data = process_debezium_message(message)
        customer_id = data.get('id')
        full_name = data.get('fullname').split(' ')
        first_name = full_name[0]
        last_name = full_name[-1]
        middle_name = ' '.join(full_name[1:-1]) if len(full_name) > 2 else ''
        gender = data.get('gender', 'Male')
        date_of_birth = data.get('date_of_birth')
        signup_date = data.get('date_join')
        
        
        # Prepare data for ClickHouse
        row = (customer_id, first_name, middle_name, last_name, gender, date_of_birth, signup_date)

        # Insert data into ClickHouse
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE,
        )
        if mode == 'c':
            client.insert('dim_customer', [row], column_names=['id', 'first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'signup_date'])
        client.close()
        logger.info(f"✅ Inserted into ClickHouse: {row}")

    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")

def stream_product(message: str):
    """Process and sink data into ClickHouse."""
    attributes = ['id', 'name', 'brand', 'price', 'stock', 'category']
    try:
        # Parse the Kafka message
        mode, data = process_debezium_message(message)
        product_id = data.get('product_id')
        product_name = data.get('product_name')
        price = data.get('original_price')
        stock = data.get('stock')
        category_id = data.get('category_id')
        brand = data.get('brand')
        
        # Prepare data for ClickHouse
        row = (product_id, product_name, brand, price, stock, category_id)

        # Insert data into ClickHouse
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE,
        )
        if mode == 'c':
            client.insert('dim_product', [row], column_names=['id', 'name', 'brand', 'price', 'stock', 'category'])
        client.close()
        logger.info(f"✅ Inserted into ClickHouse: {row}")

    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")

###################################################
#  Hàm chuyển đổi dữ liệu và ghi vào ClickHouse   #
###################################################
# def product_dim(record):
#     client = clickhouse_connect.get_client(host=CLICKHOUSE_HOST, database=CLICKHOUSE_DATABASE)
#     try:
#         # Parse JSON record
#         data = json.loads(record)
        
#         # Trích xuất các trường và chuyển đổi timestamp thành đối tượng datetime
#         id = int(data.get("id"))
#         name = data.get("name")
#         slug_name = data.get("slug_name")
#         description = data.get("description")
#         category = data.get("category")
#         version = data.get("version")
        
#         # Chuẩn bị dữ liệu để chèn vào ClickHouse
#         row = (id, name, slug_name, description, category, version)
        
#         # Ghi dữ liệu vào ClickHouse
#         client.insert('product_dim', [row])
#         logger.info(f"Ghi thành công bản ghi: {row}")

#     except Exception as e:
#         logger.error(f"Lỗi khi xử lý bản ghi: {e}")
#     client.close()

# def product():
#     df_p = pd.read_csv('Database/products.csv')
#     df_c = pd.read_csv('Database/categories.csv')
#     df_p = df_p[['product_id','product_name','brand','original_price','stock','category_id']]
#     df_p['category'] = df_p['category_id'].map(df_c.set_index('category_id')['name'])
#     df_p = df_p.drop(columns=['category_id'])
#     df_p.to_csv('dim_product.csv',index=False)


def main() -> None:
    """Main flow controller"""

    # Initialize environment
    env = initialize_env()
    logger.info("✅ Initializing environment")

    # Define source and sinks
    kafka_source = configure_source(f"{KAFKA_HOST}:{KAFKA_PORT}")
    logger.info("🐿️ Configuring source and sinks")

    data_stream = env.from_source(
        kafka_source, WatermarkStrategy.no_watermarks(), "Kafka sensors topic"
    )
    logger.info("🙊 Create a DataStream from the Kafka source and assign watermarks")

    # Áp dụng hàm xử lý cho mỗi message
    data_stream.map(
        transform_and_sink_to_clickhouse,
        output_type=Types.STRING()
    )
    data_stream.print()

    # logger.info("🚀 Ready to sink data")
    # data_stream.map(lambda record: process_message(record))

    # Thực thi job Flink
    env.execute("Test recieve data from Kafka")

if __name__ == "__main__":
    main()
