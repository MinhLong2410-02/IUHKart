import os
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError, ExpiredSignatureError
from typing import Dict
try:
    from dotenv import load_dotenv
    load_dotenv('./.env')
except ModuleNotFoundError:
    pass

# Secret key to encode/decode the JWT tokens
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()  


def decode_jwt(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
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
    return payload 
