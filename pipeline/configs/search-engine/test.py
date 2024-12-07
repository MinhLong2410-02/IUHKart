from kafka import KafkaConsumer
from dotenv import load_dotenv
import os, requests, json
from dotenv import load_dotenv
from uuid import uuid4
from pprint import pprint
load_dotenv()
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

import base64
import json

def decode_base64_fields(record: str) -> str:
    data = json.loads(record)
    
    if 'original_price' in data and isinstance(data['original_price'], str):
        try:
            decoded_price = base64.b64decode(data['original_price']).decode('utf-8')
            data['original_price'] = float(decoded_price)
        except Exception as e:
            # Xử lý lỗi nếu giải mã không thành công
            data['original_price'] = None

    if 'ratings' in data and isinstance(data['ratings'], str):
        try:
            decoded_ratings = base64.b64decode(data['ratings']).decode('utf-8')
            data['ratings'] = float(decoded_ratings)
        except Exception as e:
            # Xử lý lỗi nếu giải mã không thành công
            data['ratings'] = None

    return json.dumps(data)

def decode_message(message: str):
    """Phân tích thông điệp Kafka và trích xuất thông tin thay đổi."""
    try:
        message_json = json.loads(message)
        # payload = message_json.get('payload', {})
        operation = message_json.get('op')
        before = message_json.get('before')
        after = message_json.get('after')

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
        print("🚀 Đang lắng nghe Kafka ...")
        for message in consumer:
            mode, data = decode_message(message.value)
            print(data)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()