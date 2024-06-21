from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import current_user
from ..models import User, Message
from ..schemas import MessageIn, MessageOut, DecryptIn, DecryptOut
from ..crypto import encrypt_message, decrypt_message, decrypt_private_key


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("", response_model=MessageOut)
def send(body: MessageIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if len(body.body) > 4096:
        raise HTTPException(400, "body too long")
    recipient = db.query(User).filter(User.email == body.recipient_email).first()
    if not recipient:
        raise HTTPException(404, "recipient not found")
    ct, wrapped = encrypt_message(body.body, recipient.public_key.encode())
    m = Message(sender_id=user.id, recipient_id=recipient.id, ciphertext=ct, encrypted_key=wrapped)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.get("/inbox", response_model=list[MessageOut])
def inbox(limit: int = 50, offset: int = 0, db: Session = Depends(get_db), user: User = Depends(current_user)):
    return db.query(Message).filter(Message.recipient_id == user.id).order_by(Message.created_at.desc()).limit(limit).offset(offset).all()


@router.post("/{mid}/decrypt", response_model=DecryptOut)
def decrypt(mid: int, body: DecryptIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    m = db.get(Message, mid)
    if not m or m.recipient_id != user.id:
        raise HTTPException(404, "not found")
    try:
        priv = decrypt_private_key(user.encrypted_private_key, body.passphrase)
    except Exception:
        raise HTTPException(401, "bad passphrase")
    plaintext = decrypt_message(m.ciphertext, m.encrypted_key, priv)
    return DecryptOut(id=m.id, body=plaintext)
