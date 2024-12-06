from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import os, requests
try:
    from dotenv import load_dotenv
    load_dotenv('./.env')
except ModuleNotFoundError:
    pass

TEXT_EMBEDDING_URL = os.getenv('TEXT_EMBEDDING_URL')
QDRANT_HOST = os.getenv('QDRANT_HOST')
QDRANT_PORT = os.getenv('QDRANT_PORT')


client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

'''Tạo collection product từ ban đầu nếu chưa tồn tại'''
if 'product' not in [c.name for c in client.get_collections().collections]:
    client.create_collection(
        collection_name='product',
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    
def _check_exist(collection_name):
    return collection_name in [c.name for c in client.get_collections().collections]

def _get_points(collection_name, product_id):
    res = client.scroll(
        collection_name=collection_name,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="product_id",
                    match=models.MatchValue(value=product_id),
                )
            ]
        )
    )[0]
    return res

def getTextEmbedding(text: str):
    response = requests.get(TEXT_EMBEDDING_URL + '?q=' + text)
    vector = response.json()['embedding'] if response.status_code == 200 else None
    return vector