from fastapi import FastAPI, status
from fastapi import Depends, HTTPException
from schemas import TokenData, Product
from fastapi.middleware.cors import CORSMiddleware
from authorization import get_current_user
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
                  product: Product, 
                  current_user: TokenData = Depends(get_current_user)):
    user_id = current_user['user_id']
    return current_user

