import os, json
import logging
from pyflink.common import Types, WatermarkStrategy
from utils import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def stream_province(message: json):
    """Process and sink data into ClickHouse."""
    # attributes = ['id', 'content', 'rating', 'sentiment_score', 'date_id', 'product_id', 'customer_id', 'store_id']
    try:
        pg = Postgres()
        logger.info(f"\n🟢 Connect storage stream successfully!")
        # Parse the Kafka message
        mode, data = decode_message(message)
        province_id = data.get('province_id')
        province_name = data.get('province_name')
        if mode != "Delete":
            pg.upsert(data=(province_id, province_name), table_name="province", conflict_target="id")
            logger.info(f"\n🟢 Id: {province_id}")
        pg.close()
        # if len(data)==0 and mode != "Delete":
        #     client = get_clickhouse_client()
        #     row = (id, content, rating, date_id, product_id, customer_id)
        #     client.insert('fact_review', [row], column_names=['id', 'content', 'rating', 'date_id', 'product_id', 'customer_id'])
        #     client.close()
    except Exception as e:
        logger.error(f"\n❌ Error processing message: {e}")
    print('-'*120)

def main() -> None:
    """Main flow controller"""
    # Initialize environment
    env = initialize_env()
    # Define source and sinks
    kafka_source = configure_source(topic='postgresDB.public.provinces')
    data_stream = env.from_source(
        kafka_source, WatermarkStrategy.no_watermarks(), "Kafka sensors topic"
    )
    data_stream.map(
        stream_province,
        output_type=Types.STRING()
    )
    print("\n")
    data_stream.print()
    env.execute("Stream province job")

if __name__ == "__main__":
    main()
