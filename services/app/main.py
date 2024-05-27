from fastapi import FastAPI, HTTPException
from app.schemas import InsertPointRequestBody, UpdatePointRequestBody
from uuid import uuid4
from app.qdrant_base import client, _check_exist, _get_points, PointStruct, models, getTextEmbedding

fastapi_app = FastAPI()


## ----- Base -----
@fastapi_app.get("/")
async def root():
    return {"message": "api-qdrant"}

## ----- CRUD -----
@fastapi_app.get("/collections", status_code=200)
async def get_collections():
    '''xem tất cả các collection hiện có'''
    return {'collections': [c.name for c in client.get_collections().collections]}

@fastapi_app.get("/collections/{collection_name}", status_code=200)
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

# insert a new point
@fastapi_app.post("/collections/{collection_name}/insert", status_code=201)
async def insert_point(collection_name:str, request: InsertPointRequestBody):
    '''thêm 1 point mới vào collection_name'''
    
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    vector = getTextEmbedding(request.slug)
    
    if vector is None:
        return {'detail': 'Vector is None'}
    payload = {
        'product_id': request.product_id,
        'product_name': request.product_name,
        'product_image_url': request.product_image_url
    }
    point = PointStruct(id=str(uuid4()),
                        vector=vector,
                        payload=payload
            )
    client.upsert(collection_name=collection_name, points=[point])
    return {'payload': payload}

# update a point
@fastapi_app.put("/collections/{collection_name}/update", status_code=200)
async def update_point(collection_name: str, request: UpdatePointRequestBody):
    '''Update a point in collection_name'''
    if not _check_exist(collection_name):
        raise HTTPException(status_code=404, detail="Collection name not found!")
    points = _get_points(collection_name, request.product_id)
    if len(points) == 0:
        raise HTTPException(status_code=404, detail="Product ID not found!")
    p = points[0]
    vector = p.vector
    if request.slug:
        vector = getTextEmbedding(request.slug)
        if vector is None:
            return {'detail': 'Vector is None'}
    payload = p.payload
    if request.product_name:
        payload["product_name"] = request.product_name
    if request.product_image_url:
        payload["product_image_url"] = request.product_image_url
    point = PointStruct(id=p.id, vector=vector, payload=payload)
    client.upsert(collection_name=collection_name, points=[point])
    return {'payload': payload}

# delete a point
@fastapi_app.delete("/collections/{collection_name}/delete", status_code=200)
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
@fastapi_app.get("/collections/{collection_name}/search", status_code=200)
async def search(collection_name:str=None, slug:str=None, limit:int=10, thresh:float=0.0):
    '''tìm kiếm các point gần nhất với slug trong collection_name, lấy theo giới hạn và ngưỡng'''
    if slug is None:
        raise HTTPException(status_code=404, detail="Slug not found!")
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    
    vector = getTextEmbedding(slug)
    if vector is None:
        return {'detail': 'Vector is None'}
    res = client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=limit
    )
    res = [{'score':i.score, 'payload':i.payload} for i in res if i.score >= thresh]
    return {'results': res}