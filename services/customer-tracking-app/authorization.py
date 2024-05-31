from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from schemas import TokenData
from dotenv import load_dotenv
import os
load_dotenv(".env")

JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
NAME = os.getenv("NAME")
wd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("user_name")
        user_id = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

# Dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token or expired token")