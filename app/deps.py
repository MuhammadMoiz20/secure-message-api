from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .db import get_db
from .auth import read_token
from .models import User


def current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing token")
    uid = read_token(authorization[7:])
    if not uid:
        raise HTTPException(401, "invalid token")
    u = db.get(User, uid)
    if not u:
        raise HTTPException(401, "no user")
    return u
