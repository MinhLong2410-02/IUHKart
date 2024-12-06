from kafka import KafkaConsumer
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import os, requests, json
from dotenv import load_dotenv
from uuid import uuid4
from pprint import pprint
load_dotenv()
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
URL_EMBEDDING = os.getenv("URL_EMBEDDING")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")

def decode_message(message: str):
    """Phân tích thông điệp Kafka và trích xuất thông tin thay đổi."""
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

        print(f"Action: {action}")
        return operation, data

    except json.JSONDecodeError as e:
        print(f"Lỗi khi giải mã JSON: {e}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

def collection_init():
    collection_name='product'
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    if collection_name in [c.name for c in client.get_collections().collections]:
        # client.delete_collection(collection_name=collection_name)
        print(f"🔍 Collection {collection_name} already exists")
    else:
        client.create_collection(collection_name=collection_name, vectors_config=VectorParams(size=384, distance=Distance.COSINE))
        print(f"✅ Collection {collection_name} initialized")
    client.close()

def insert_qdrant(message):
    collection_name='product'
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    operation, data = decode_message(message)

    if operation == 'd':
        # delete point with product_id
        client.delete(collection_name=collection_name, point_ids=[data['product_id']])
        print(f"🟢 Deleted from Qdrant: {data['product_name']}")
    else:
        # upsert point with product_id
        vector = requests.get(f"{URL_EMBEDDING}/embedding?q={data['slug']}").json()['embedding']
        payload = {
            'product_id': data['product_id'],
            'product_name': f"{data['product_name']}",
            'product_image_url': None
        }

        if vector is None:
            raise Exception("❌ Cannot get embedding vector")
        
        point = PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload=payload
        )
        client.upsert(
            collection_name=collection_name, 
            points=[point]
        )
        print(f"🟢 Inserted into Qdrant: {payload['product_name']}")
    client.close()

def main():

    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],  # Địa chỉ và cổng Kafka broker
            auto_offset_reset='earliest',  # Bắt đầu từ offset đầu tiên
            enable_auto_commit=True,        # Tự động commit offset
            group_id='qdrant',       # ID nhóm consumer
            value_deserializer=lambda m: m.decode('utf-8')  # Giải mã giá trị
        )
        collection_init()
        print("🖋️ Start consuming...")
        for message in consumer:
            pprint(message.value)
            # insert_qdrant(message.value)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()