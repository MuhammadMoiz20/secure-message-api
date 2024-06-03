from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from .config import settings


pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(p: str) -> str:
    return pwd.hash(p)


def verify_password(p: str, h: str) -> bool:
    return pwd.verify(p, h)


def make_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.jwt_ttl_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def read_token(token: str) -> int | None:
    try:
        d = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return int(d["sub"])
    except JWTError:
        return None
