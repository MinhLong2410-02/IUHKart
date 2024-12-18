from fastapi import FastAPI, HTTPException, Request, Path, Query, Depends
from schemas import InsertPointRequestBody, UpdatePointRequestBody, SearchQueryParams
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from qdrant_base import (
    client, 
    _check_exist, 
    _get_points, 
    PointStruct, 
    models, 
    getTextEmbedding, 
    VectorParams, 
    Distance
)
from utils import search_tracking, remove_vietnamese_accents

app = FastAPI()
allowed_origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST"],
    allow_headers=["*"],
)

## ----- Base -----
@app.get("/")
async def root():
    return {"message": "api-qdrant"}

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

# insert a new point
@app.post("/collections/{collection_name}/insert", status_code=201)
async def insert_point(collection_name:str, request: InsertPointRequestBody):
    '''thêm 1 point mới vào collection_name'''
    
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    vector = getTextEmbedding(request.slug)
    
    if vector is None:
        return {'detail': 'Vector is None'}
    payload = {
        'product_id': request.product_id,
        'product_name': request.product_name
    }
    point = PointStruct(id=str(uuid4()),
                        vector=vector,
                        payload=payload
            )
    client.upsert(collection_name=collection_name, points=[point])
    return {'payload': payload}

# update a point
@app.put("/collections/{collection_name}/update", status_code=200)
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
    # if request.product_image_url:
    #     payload["product_image_url"] = request.product_image_url
    point = PointStruct(id=p.id, vector=vector, payload=payload)
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

# search
@app.get("/collections/{collection_name}/search", status_code=200)
async def search(
    request: Request,
    collection_name: str = Path(..., description="Name of the collection"), 
    query_params: SearchQueryParams = Depends(),
):
    '''tìm kiếm các point gần nhất với slug trong collection_name, lấy theo giới hạn và ngưỡng'''
    slug = query_params.slug
    limit = query_params.limit
    thresh = query_params.thresh
    
    access_token = request.headers.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token missing or invalid")
    
    if slug is None:
        raise HTTPException(status_code=404, detail="Slug not found!")
    if collection_name is None or _check_exist(collection_name)==False:
        raise HTTPException(status_code=404, detail="Collection name not found!")
    slug = remove_vietnamese_accents(slug)
    vector = getTextEmbedding(slug)
    if vector is None:
        return {'detail': 'Vector is None'}
    products = client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=limit
    )
    product_ids = list(set([product.payload['product_id'] for product in products]))
    tracking_status = search_tracking(product_ids, access_token)
    res = [{'score':i.score, 'payload':i.payload} for i in products if i.score >= thresh]
    return {'results': res, 'tracking_status': tracking_status}
