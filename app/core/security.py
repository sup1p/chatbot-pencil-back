from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

def create_token(data: dict) -> str:
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    encoded = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
    return encoded

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except:
        raise ValueError("Token verification failed")
