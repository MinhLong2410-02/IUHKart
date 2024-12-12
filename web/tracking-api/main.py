from typing import Union, List
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from pymongo.collection import Collection
from database import get_db
from auth import get_current_user
from pydantic import BaseModel

app = FastAPI()
class TrackEventRequest(BaseModel):
    event_type: str
    product_ids: List[str]
# Define behavior weights globally for easy reuse
BEHAVIOR_WEIGHTS = {
    "search": 1,
    "view": 3,
    "add_to_cart": 5,
    "purchase": 10
}

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/track")
async def track_event(
    request: TrackEventRequest,
    db: Collection = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    event_type = request.event_type
    product_ids = request.product_ids
    if event_type not in BEHAVIOR_WEIGHTS:
        raise HTTPException(status_code=400, detail="Invalid event type")

    user_id = user.get("user_id")

    weight = BEHAVIOR_WEIGHTS[event_type]

    if isinstance(product_ids, str):
        product_ids = [product_ids]

    db.behaviors.insert_many([
        {
            "user_id": user_id,
            "event_type": event_type,
            "product_id": product_id,
            "weight": weight,
            "timestamp": datetime.utcnow(),
        } for product_id in product_ids
    ])

    return {"status": "success"}

