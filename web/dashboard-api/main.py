from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import get_current_user, generate_metabase_embed_url
from pydantic import BaseModel, Field, ValidationError


app = FastAPI()


class EmbedURLResponse(BaseModel):
    embed_url: str

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST","OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.get("/dashboard", response_model=EmbedURLResponse)
async def get_dashboard_url(user: dict = Depends(get_current_user)):
    shop_id = user.get("vendor_id", user.get("user_id"))
    
    embed_url = generate_metabase_embed_url(shop_id)
    return {"embed_url": embed_url}


