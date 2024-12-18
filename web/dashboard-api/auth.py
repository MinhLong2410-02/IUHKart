import os, requests
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError, ExpiredSignatureError
from typing import Dict
from datetime import datetime, timedelta
try:
    from dotenv import load_dotenv
    load_dotenv('./.env')
except ModuleNotFoundError:
    pass

AUTHENTICATE_API = os.getenv("AUTHENTICATE_API")

METABASE_URL = os.getenv("METABASE_URL")
METABASE_EMBEDDING_SECRET = os.getenv("METABASE_EMBEDDING_SECRET")
METABASE_DASHBOARD_ID=1

security = HTTPBearer()


def decode_jwt(token: str) -> Dict:
    try:
        payload = requests.post(AUTHENTICATE_API, data={'token': token})
        if payload.status_code != 200:
            raise HTTPException(
                status_code=401, detail="Invalid or expired JWT token"
            )
        return payload.json()
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="JWT token has expired"
        )
    except PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid or expired JWT token"
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict:
    token = credentials.credentials
    payload = decode_jwt(token)
    return payload['decoded_token']

def generate_metabase_embed_url(shop_id: str) -> str:
    payload = {
        "resource": {
            "dashboard": METABASE_DASHBOARD_ID
        },
        "params": {
            "shop_id": shop_id
        },
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expiration time
    }

    token = jwt.encode(payload, METABASE_EMBEDDING_SECRET, algorithm='HS256')
    embed_url = f"{METABASE_URL}embed/dashboard/{token}#bordered=true&titled=true"

    return embed_url