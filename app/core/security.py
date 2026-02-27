
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

pwd = CryptContext(schemes=["bcrypt"])
ALGO = "HS256"

def hash_password(password: str):
    return pwd.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd.verify(plain_password, hashed_password)

def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)