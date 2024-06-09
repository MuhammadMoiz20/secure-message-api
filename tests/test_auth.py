def test_register_login(client):
    r = client.post("/auth/register", json={"email": "a@b.com", "password": "pw12345", "passphrase": "ph"})
    assert r.status_code == 200
    tok = r.json()["access_token"]
    assert tok

    r2 = client.post("/auth/login", json={"email": "a@b.com", "password": "pw12345"})
    assert r2.status_code == 200


def test_bad_login(client):
    client.post("/auth/register", json={"email": "x@y.com", "password": "pw12345", "passphrase": "ph"})
    r = client.post("/auth/login", json={"email": "x@y.com", "password": "wrong"})
    assert r.status_code == 401
