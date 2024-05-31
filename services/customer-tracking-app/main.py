from fastapi import FastAPI, status
from fastapi import Depends, HTTPException
from schemas import TokenData, Product
from fastapi.middleware.cors import CORSMiddleware
from database import redis_client, track_db, cursor, execute_query
from authorization import get_current_user
import json

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


@app.get("")
@app.get("/checkstatus")
async def root(current_user: TokenData = Depends(get_current_user)):
    user_id = current_user['user_id']   
    return {
        'status': 'ok',
        'user': user_id
    }



@app.post("/api/v1/keep-track", status_code=status.HTTP_202_ACCEPTED,)
async def keepTrack(
                  product: Product = None, 
                  current_user: TokenData = Depends(get_current_user)):
    user_id = current_user['user_id']
    
    if user_id not in track_db.list_collection_names() or product == None:
        cursor.execute(f"SELECT product_id FROM product ORDER BY ratings DESC LIMIT 20;")
        rows = cursor.fetchall()
        product_ids = [row[0] for row in rows]
        product_ids.append(user_id)
        execute_query('''UPDATE customer
            SET recommend_product_ids  = '{%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s}'
            WHERE WHERE user_id = %s;
        ''', product_ids)
        track_db.create_collection(str(user_id))
        return current_user
    user_collection = track_db[user_id]
    user_collection.insert_one(product.model_dump())
    
    message = json.dumps({'user_id': user_id, 'product_id': product.product_id})
    redis_client.publish('recommendation', message)
    return current_user

