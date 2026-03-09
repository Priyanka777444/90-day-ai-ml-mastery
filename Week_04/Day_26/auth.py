from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

#secret keys for jwt (JSOn wen token)
SECRET_KEY = "key-will-be-changed-in-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

#fake users database (replace with real bd later)
USERS_DB = {
    "priyanka": {
        "username": "priyanka",
        "hashed_password": None  # will set below
    },
    "client1": {
        "username": "client1", 
        "hashed_password": None
    }
}

#hash password on startup
USERS_DB["priyanka"]["hashed_password"] = pwd_context.hash("password123")
USERS_DB["client1"]["hashed_password"] = pwd_context.hash("client123")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = USERS_DB.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
    
