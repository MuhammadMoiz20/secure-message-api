# secure-message-api

fastapi service for sending end-to-end encrypted messages between users.

## how it works

- each user has an rsa keypair generated on signup
- the private key is encrypted with the user's passphrase (scrypt + fernet) and stored
- sending a message: server generates a fresh symmetric key, encrypts the body with it (fernet), and wraps the symmetric key with the recipient's public rsa key
- only the recipient can decrypt: they supply their passphrase, server derives the kdf key, decrypts the private key in memory, unwraps the symmetric key, and decrypts the body

## endpoints

- `POST /auth/register` - email, password, passphrase
- `POST /auth/login` - returns jwt
- `POST /messages` - send (requires auth)
- `GET /messages/inbox` - list
- `POST /messages/{id}/decrypt` - returns plaintext

## run

```
make install
make run
```

## test
```
make test
```

## docker
```
docker compose up --build
```

## known limitations
- bcrypt cost is library default; consider tuning
- no refresh tokens, no token revocation list
- single sqlite db; not designed for horizontal scaling as-is
- no rate limit on `/messages/*/decrypt` - add if abuse becomes an issue

## security notes
- passphrase is never stored - it's only used in-memory to unwrap the private key on decrypt
- a stolen db dump leaks ciphertexts + encrypted private keys, but not plaintext or private keys
- jwt is bearer-only (no refresh) - keep ttl short in production
