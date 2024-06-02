from pydantic import BaseModel, EmailStr
from datetime import datetime


class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    passphrase: str  # used to encrypt the private key at rest


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageIn(BaseModel):
    recipient_email: EmailStr
    body: str


class MessageOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DecryptIn(BaseModel):
    passphrase: str


class DecryptOut(BaseModel):
    id: int
    body: str
