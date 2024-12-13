import os, json
import logging
import clickhouse_connect

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
    env.set_parallelism(1)

    # Get current directory
    root_dir_list = __file__.split("/")[:-2]
    root_dir = "/".join(root_dir_list)

    # Adding the jar to the flink streaming environment
    env.add_jars(
        f"file://{root_dir}/lib/flink-sql-connector-kafka-3.1.0-1.18.jar",
    )
    return env

def decode_message(message: str):
    """Decode Kafka message and extract change data."""
    try:
        message_json = json.loads(message)
        operation = message_json.get('op')
        before = {k.split(".")[-1]: v for k, v in message_json.items() if k.startswith('before') and k.split(".")[-1]}
        after = {k.split(".")[-1]: v for k, v in message_json.items() if k.startswith('after') and k.split(".")[-1]}
        if operation == 'c':
            return 'Create', after
        elif operation == 'u':
            return 'Update', after
        elif operation == 'r':
            return 'Read', after
        elif operation == 'd':
            return 'Delete', before
        else:
            return 'Unknown', None
    except Exception as e:
        print(f"Error decoding message: {e}")
        return None, None

def configure_source(server:str, topic:str,  earliest:bool = False) -> KafkaSource:
    """Makes kafka source initialization"""
    properties = {
        "bootstrap.servers": server,
        "group.id": f"flink_{topic.split('.')[-1]}_consumer",
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

# def stream_dim_customer(message: str, client):
#     """Process and sink data into ClickHouse."""
#     attributes = ['id', 'first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'signup_date']
#     print("\n🔵 Processing customer")
#     try:
#         # Parse the Kafka message
#         mode, data = decode_message(message)
#         customer_id = data.get('id')
#         full_name = data.get('fullname').split(' ')
#         first_name = full_name[0]
#         last_name = full_name[-1]
#         middle_name = ' '.join(full_name[1:-1]) if len(full_name) > 2 else ''
#         gender = data.get('gender', 'Male')
#         date_of_birth = data.get('date_of_birth')
#         signup_date = data.get('date_join')
        
        
#         # Prepare data for ClickHouse
#         row = (customer_id, first_name, middle_name, last_name, gender, date_of_birth, signup_date)

#         # # Insert data into ClickHouse
#         # client = get_clickhouse_client()
#         # if mode == 'c':
#         #     client.insert('dim_customer', [row], column_names=['id', 'first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'signup_date'])
#         # client.close()
#         # logger.info(f"✅ Inserted into ClickHouse: {row}")

#     except Exception as e:
#         logger.error(f"❌ Error processing message: {e}")
#     print('-'*120)

# def stream_dim_store(message: str):
#     """Process and sink data into ClickHouse."""
#     print("\n🔵 Processing store")
#     try:
#         mode, data = decode_message(message)
#         _id = data.get('id')
#         shop_name = data.get('name')
#         establish_date = data.get('date_join')
        
#         # Prepare data for ClickHouse
#         row = (_id, shop_name, establish_date)

#         client = get_clickhouse_client()
#         if mode == 'c':
#             client.insert('dim_store', [row], column_names=['id', 'shop_name', 'establish_date'])
#         client.close()
#         logger.info(f"✅ Inserted into ClickHouse: {row}")

#     except Exception as e:
#         logger.error(f"❌ Error processing message: {e}")
#     print('-'*120)

# def stream_product(message: str):
#     """Process and sink data into ClickHouse."""
#     attributes = ['id', 'name', 'brand', 'price', 'stock', 'category']
#     print("\n🔵 Processing product")
#     try:
#         client = get_clickhouse_client()
#         query_result = client.query('SELECT * FROM category')
#         mapper = {i[0]:i[1] for i in query_result.result_set}

#         # Parse the Kafka message
#         mode, data = decode_message(message)
#         product_id = data.get('product_id')
#         product_name = data.get('product_name')
#         price = data.get('original_price')
#         stock = data.get('stock')
#         category = mapper[data.get('category_id')]
#         brand = data.get('brand')
#         shop_id = data.get('vendor_id')
        
#         # Prepare data for ClickHouse
#         row = (product_id, product_name, brand, price, stock, category)
        
#         if mode == 'c':
#             client.insert('dim_product', [row], column_names=['id', 'name', 'brand', 'price', 'stock', 'category'])
#             client.insert('product_store', [(shop_id, product_id)], column_names=['product_id', 'store_id'])
#         client.close()
#         logger.info(f"✅ Inserted into ClickHouse: {row}")

#     except Exception as e:
#         logger.error(f"❌ Error processing message: {e}")
#     print('-'*120)

# def stream_category(message: str):
#     """Process and sink data into ClickHouse."""
#     try:
#         # Parse the Kafka message
#         mode, data = decode_message(message)
#         category_id = data.get('category_id')
#         category_name = data.get('category_name')
        
#         # Prepare data for ClickHouse
#         row = (category_id, category_name)

#         # Insert data into ClickHouse
#         client = get_clickhouse_client()
#         if mode == 'c':
#             client.insert('category', [row], column_names=['id', 'name'])
#         client.close()
#         logger.info(f"✅ Inserted into ClickHouse: {row}")

#     except Exception as e:
#         logger.error(f"❌ Error processing message: {e}")

def stream_review(message: json):
    """Process and sink data into ClickHouse."""
    # attributes = ['id', 'content', 'rating', 'sentiment_score', 'date_id', 'product_id', 'customer_id', 'store_id']
    print("\n🐿️ Processing review")
    try:
        client = get_clickhouse_client()
        # query_result = client.query('SELECT * FROM product_store')
        # mapper = {i[0]:i[1] for i in query_result.result_set}

        # Parse the Kafka message
        mode, data = decode_message(message)
        id = data.get('review_id')
        content = data.get('review_content')
        rating = data.get('review_rating')
        date_id = data.get('review_date')
        product_id = data.get('product_id_id')
        customer_id = data.get('customer_id_id')
        # store_id = mapper.get(product_id)
        
        # Prepare data for ClickHouse
        row = (id, content, rating, date_id, product_id, customer_id)
        
        if mode == 'c':
            client.insert('fact_review', [row], column_names=['id', 'content', 'rating', 'date_id', 'product_id', 'customer_id'])
        client.close()
        logger.info(f"\n🟢 Inserted into ClickHouse: {row}")

    except Exception as e:
        logger.error(f"\n❌ Error processing message: {e}")
    print('-'*120)

def main() -> None:
    """Main flow controller"""

    # Initialize environment
    env = initialize_env()
    logger.info("🟢 Initializing environment")

    # Define source and sinks
    kafka_source = configure_source(f"{KAFKA_HOST}:{KAFKA_PORT}", 'postgresDB.public.reviews')
    logger.info("🟢 Configuring source and sinks")

    data_stream = env.from_source(
        kafka_source, WatermarkStrategy.no_watermarks(), "Kafka sensors topic"
    )
    logger.info("🟢 Create a DataStream from the Kafka source and assign watermarks")

    # Áp dụng hàm xử lý cho mỗi message
    data_stream.map(
        stream_review,
        output_type=Types.STRING()
    )

    # Thực thi job Flink
    env.execute("Flink ETL Job")

if __name__ == "__main__":
    main()
