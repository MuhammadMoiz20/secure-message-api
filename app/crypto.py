from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import base64


def generate_rsa_keypair():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return priv_pem, pub_pem


def _kdf(passphrase: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(passphrase.encode())


def encrypt_private_key(priv_pem: bytes, passphrase: str) -> bytes:
    salt = os.urandom(16)
    key = _kdf(passphrase, salt)
    f = Fernet(base64.urlsafe_b64encode(key))
    return salt + f.encrypt(priv_pem)


def decrypt_private_key(blob: bytes, passphrase: str) -> bytes:
    salt, ct = blob[:16], blob[16:]
    key = _kdf(passphrase, salt)
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.decrypt(ct)


def rsa_encrypt(pub_pem: bytes, data: bytes) -> bytes:
    pub = serialization.load_pem_public_key(pub_pem)
    return pub.encrypt(data, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))


def rsa_decrypt(priv_pem: bytes, data: bytes) -> bytes:
    priv = serialization.load_pem_private_key(priv_pem, password=None)
    return priv.decrypt(data, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))


def encrypt_message(body: str, pub_pem: bytes):
    """encrypt body with a fresh AES key, encrypt the key with recipient pubkey"""
    key = Fernet.generate_key()
    f = Fernet(key)
    ct = f.encrypt(body.encode())
    wrapped = rsa_encrypt(pub_pem, key)
    return ct, wrapped


def decrypt_message(ct: bytes, wrapped: bytes, priv_pem: bytes) -> str:
    key = rsa_decrypt(priv_pem, wrapped)
    f = Fernet(key)
    return f.decrypt(ct).decode()
