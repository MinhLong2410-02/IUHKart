from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from pymongo.collection import Collection
from database import get_db
from auth import get_current_user

app = FastAPI()

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
    allow_origins=[
        "http://localhost",  
        "http://*.iuhkart.systems",  
        "https://*.iuhkart.systems" 
    ],
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
    event_type: str,
    product_id: str,
    db: Collection = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if event_type not in BEHAVIOR_WEIGHTS:
        raise HTTPException(status_code=400, detail="Invalid event type")

    user_id = user.get("user_id")

    weight = BEHAVIOR_WEIGHTS[event_type]

    db.behaviors.insert_one({
        "user_id": user_id,
        "event_type": event_type,
        "product_id": product_id,
        "weight": weight,
        "timestamp": datetime.utcnow(),
    })

    return {"status": "success"}