from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    public_key = Column(Text, nullable=False)
    encrypted_private_key = Column(LargeBinary, nullable=False)  # encrypted with passphrase
    created_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    ciphertext = Column(LargeBinary, nullable=False)
    encrypted_key = Column(LargeBinary, nullable=False)  # AES key encrypted with recipient pubkey
    created_at = Column(DateTime, default=datetime.utcnow)
