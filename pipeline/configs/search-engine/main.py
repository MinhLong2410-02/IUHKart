from kafka import KafkaConsumer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import os, requests, json
from uuid import uuid4
from dotenv import load_dotenv
from time import time
import sys

load_dotenv()
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
URL_EMBEDDING = os.getenv("URL_EMBEDDING")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")

def create_consumer():
    """Create Kafka consumer instance."""
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='qdrant',
        value_deserializer=lambda m: m.decode('utf-8')
    )

def decode_message(message: str):
    """Decode Kafka message and extract change data."""
    try:
        message_json = json.loads(message)
        operation = message_json.get('op')
        before = {k.split(".")[-1]: v for k, v in message_json.items() if k.startswith('before') and k.split(".")[-1] in ("product_id", "product_name", "slug")}
        after = {k.split(".")[-1]: v for k, v in message_json.items() if k.startswith('after') and k.split(".")[-1] in ("product_id", "product_name", "slug")}
        if operation == 'c':
            return 'create', after
        elif operation == 'u':
            return 'update', after
        elif operation == 'd':
            return 'delete', before
        else:
            return 'unknown', None
    except Exception as e:
        print(f"Error decoding message: {e}")
        return None, None

def process_batch(messages):
    """Process a batch of Kafka messages."""
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    points = []
    for message in messages:
        operation, data = decode_message(message)
        if not data:
            continue
        if operation == 'delete':
            client.delete(collection_name='product', point_ids=[data['product_id']])
        else:
            vector = requests.get(f"{URL_EMBEDDING}/embedding?q={data['slug']}").json().get('embedding')
            if vector:
                points.append(PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        'product_id': data['product_id'],
                        'product_name': data['product_name']
                    }
                ))
    if points:
        client.upsert(collection_name='product', points=points)
    client.close()

# def process_messages(consumer):
#     """Process messages from Kafka in batches or individually."""
#     batch = []
#     try:
#         for message in consumer:
#             batch.append(message.value)
#             if len(batch) >= 100 or len(batch) == 1:  
#                 process_batch(batch)
#                 batch.clear()
#         if batch:
#             process_batch(batch)
#     except Exception as e:
#         print(f"Error while processing messages: {e}")

def process_messages(consumer):
    """Process messages from Kafka in batches or individually."""
    batch = []
    batch_start_time = None
    BATCH_SIZE = 100
    BATCH_TIMEOUT = 60  # 1 phut
    batch_index = 0
    try:
        while True:
            # Thời gian chờ tối đa để lấy tin nhắn (timeout)
            message = consumer.poll(timeout_ms=0.5)
            if message:
                for tp, messages in message.items():
                    for msg in messages:
                        if not batch:
                            # Đặt thời gian bắt đầu khi thêm tin nhắn đầu tiên vào lô
                            batch_start_time = time()
                        batch.append(msg.value)

                        if len(batch) >= BATCH_SIZE:
                            batch_index += 1
                            print(f"🟢 Processing batch {batch_index} FULL")
                            sys.stdout.flush()
                            process_batch(batch)
                            batch.clear()
                            batch_start_time = None  # Reset thời gian bắt đầu lô
            # Kiểm tra nếu có lô và đã đạt thời gian chờ
            if batch and batch_start_time:
                elapsed_time = time() - batch_start_time
                if elapsed_time >= BATCH_TIMEOUT:
                    batch_index += 1
                    print(f"🟢 Processing batch {batch_index} TIMEOUT")
                    sys.stdout.flush()
                    process_batch(batch)
                    batch.clear()
                    batch_start_time = None  # Reset thời gian bắt đầu lô

    except Exception as e:
        print(f"Error while processing messages: {e}")
    finally:
        # Xử lý lô còn lại khi kết thúc
        if batch:
            batch_index += 1
            print(f"🟢 Processing batch {batch_index} FINAL")
            sys.stdout.flush()
            process_batch(batch)

def main():
    consumer = create_consumer()
    print("🖋️ Starting to consume messages...")
    sys.stdout.flush()
    process_messages(consumer)

if __name__ == "__main__":
    main()
