from kafka import KafkaConsumer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import os, requests, json
from uuid import uuid4
from dotenv import load_dotenv
from pprint import pprint
import signal
import sys

# Load environment variables
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
        # payload = message_json.get('payload', {})
        operation = message_json.get('op')
        before = message_json.get('before')
        after = message_json.get('after')

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


def collection_init():
    """Initialize Qdrant collection."""
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    collection_name = 'product'
    if collection_name not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"✅ Collection {collection_name} created")
    else:
        print(f"🔍 Collection {collection_name} already exists")
    client.close()


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
            print(vector)
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


def process_messages(consumer):
    """Process messages from Kafka in batches or individually."""
    batch = []
    try:
        for message in consumer:
            batch.append(message.value)

            # Process batch immediately if size is 1 or reaches 100
            if len(batch) >= 100 or len(batch) == 1:  
                process_batch(batch)
                batch.clear()

        # Process remaining messages in the batch (if any)
        if batch:
            process_batch(batch)

    except Exception as e:
        print(f"Error while processing messages: {e}")



def main():

    collection_init()
    consumer = create_consumer()
    print("🖋️ Starting to consume messages...")
    process_messages(consumer)


if __name__ == "__main__":
    main()
