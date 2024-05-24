from fastapi import FastAPI, HTTPException
import os, requests
from uuid import uuid4
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct

app = FastAPI()
client = QdrantClient(host='qdrant_db', port=6333)

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

## ----- Base -----
@app.get("/")
async def root():
    return {"message": "api-qdrant"}

@app.get("/env")
async def check_env():
    load_dotenv()
    return os.environ

## ----- CRUD -----
@app.get("/collections", status_code=200)
async def get_collections():
    '''xem tất cả các collection hiện có'''
    return {'collections': [c.name for c in client.get_collections().collections]}

@app.get("/collections/{collection_name}", status_code=200)
async def get_points(collection_name:str=None):
    '''xem tất cả point trong collection_name'''
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    res = client.search(
        collection_name=collection_name,
        query_vector=list(range(384))
    )
    res = [i.payload for i in res]
    return  {'payloads': res}

# create a new collection
@app.post("/collections/create", status_code=201)
async def create_collection(collection_name:str=None):
    '''tạo 1 collection mới, nếu đã tồn tại thì thôi'''
    if collection_name is None:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    res = 'existed'
    if collection_name not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        res = 'success'
    return {'detail': res}

# delete a collection
@app.delete("/collections/delete", status_code=200)
async def delete_collection(collection_name:str=None):
    '''xóa 1 collection, nếu không tồn tại thì thôi'''
    if collection_name is None:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    res = 'not found'
    if collection_name in [c.name for c in client.get_collections().collections]:
        client.delete_collection(collection_name)
        res = 'deleted'
    return {'detail': res}

# insert a new point
@app.post("/collections/{collection_name}/insert", status_code=201)
async def insert_point(collection_name:str=None, slug:str=None, product_id:int=None, product_name:str=None, product_url:str=None):
    '''thêm 1 point mới vào collection_name'''
    if slug is None:
        raise HTTPException(status_code=404, detail="Slug not found!")
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    response = requests.get(str(os.getenv('TEXT_EMBEDDING_URL')) + '?q=' + slug)
    vector = response.json()['embedding'] if response.status_code == 200 else None
    if vector is None:
        return {'detail': 'Vector is None'}
    payload = {
        'product_id': product_id,
        'product_name': product_name,
        'product_url': product_url
    }
    point = PointStruct(id=str(uuid4()),
                        vector=vector,
                        payload=payload
            )
    client.upsert(collection_name=collection_name, points=[point])
    return {'payload': payload}

# update a point
@app.put("/collections/{collection_name}/update", status_code=200)
async def update_point(collection_name:str=None, slug:str=None, product_id:int=None, product_name:str=None, product_url:str=None):
    '''cập nhật 1 point trong collection_name, neu khong them param thi giu param cu theo product_id'''
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    points = _get_points(collection_name, product_id)
    p = points[0]
    if len(points) == 0:
        return {'detail': 'ID not found!'}
    vector = p.vector
    if slug:
        response = requests.get(str(os.getenv('TEXT_EMBEDDING_URL')) + '?q=' + slug)
        vector = response.json()['embedding'] if response.status_code == 200 else None
        if vector is None:
            return {'detail': 'Vector is None'}
    payload = p.payload
    if product_name:
        payload["product_name"] = product_name
    if product_url:
        payload["product_url"] = product_url
    point = PointStruct(id=p.id,
        vector=vector,
        payload=payload
    )
    client.upsert(collection_name=collection_name, points=[point])
    return {'payload': payload}

# delete a point
@app.delete("/collections/{collection_name}/delete", status_code=200)
async def delete_point(collection_name:str=None, product_id:int=None):
    '''xóa 1 point theo product_id trong collection_name'''
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    if product_id is None:
        raise HTTPException(status_code=404, detail="Product ID not found!")
    client.delete(
        collection_name=collection_name,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="product_id",
                        match=models.MatchValue(value=product_id),
                    ),
                ],
            )
        )
    )
    return {'detail': 'deleted'}

# search
@app.get("/collections/{collection_name}/search", status_code=200)
async def search(collection_name:str=None, slug:str=None, limit:int=10, thresh:float=0.0):
    '''tìm kiếm các point gần nhất với slug trong collection_name, lấy theo giới hạn và ngưỡng'''
    if slug is None:
        raise HTTPException(status_code=404, detail="Slug not found!")
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    response = requests.get(str(os.getenv('TEXT_EMBEDDING_URL')) + '?q=' + slug)
    vector = response.json()['embedding'] if response.status_code == 200 else None
    if vector is None:
        return {'detail': 'Vector is None'}
    res = client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=limit
    )
    res = [{'score':i.score, 'payload':i.payload} for i in res if i.score >= thresh]
    return {'results': res}