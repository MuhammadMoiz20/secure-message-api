from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..schemas import RegisterIn, LoginIn, TokenOut
from ..auth import hash_password, verify_password, make_token
from ..crypto import generate_rsa_keypair, encrypt_private_key


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "email taken")
    priv, pub = generate_rsa_keypair()
    enc_priv = encrypt_private_key(priv, body.passphrase)
    u = User(
        email=body.email,
        password_hash=hash_password(body.password),
        public_key=pub.decode(),
        encrypted_private_key=enc_priv,
    )
    db.add(u)
    db.commit()
    return TokenOut(access_token=make_token(u.id))


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == body.email).first()
    if not u or not verify_password(body.password, u.password_hash):
        raise HTTPException(401, "bad credentials")
    return TokenOut(access_token=make_token(u.id))
