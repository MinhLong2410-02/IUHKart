# from dotenv import load_dotenv
# import os
# import clickhouse_connect
# load_dotenv()

# CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
# CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT")
# CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
# CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
# CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE")

# def get_clickhouse_client():
#     """Initialize ClickHouse client."""
#     client = clickhouse_connect.get_client(
#         host=CLICKHOUSE_HOST,
#         port=CLICKHOUSE_PORT,
#         username=CLICKHOUSE_USER,
#         password=CLICKHOUSE_PASSWORD,
#         database=CLICKHOUSE_DATABASE,
#     )
#     return client

# client = get_clickhouse_client()

# query_result = client.query('SELECT * FROM category')
# mapper = {i[0]:i[1] for i in query_result.result_set}
# print(mapper)

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