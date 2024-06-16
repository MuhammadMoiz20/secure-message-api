def reg(client, email, pw="pw123456", ph="ph"):
    r = client.post("/auth/register", json={"email": email, "password": pw, "passphrase": ph})
    return r.json()["access_token"]


def test_send_and_decrypt(client):
    t1 = reg(client, "alice@x.com")
    t2 = reg(client, "bob@x.com")

    r = client.post(
        "/messages",
        json={"recipient_email": "bob@x.com", "body": "hello bob"},
        headers={"Authorization": f"Bearer {t1}"},
    )
    assert r.status_code == 200
    mid = r.json()["id"]

    inbox = client.get("/messages/inbox", headers={"Authorization": f"Bearer {t2}"}).json()
    assert any(m["id"] == mid for m in inbox)

    r = client.post(
        f"/messages/{mid}/decrypt",
        json={"passphrase": "ph"},
        headers={"Authorization": f"Bearer {t2}"},
    )
    assert r.status_code == 200
    assert r.json()["body"] == "hello bob"


def test_bad_passphrase(client):
    t1 = reg(client, "a@a.com")
    t2 = reg(client, "b@b.com")
    r = client.post("/messages", json={"recipient_email": "b@b.com", "body": "x"}, headers={"Authorization": f"Bearer {t1}"})
    mid = r.json()["id"]
    r = client.post(f"/messages/{mid}/decrypt", json={"passphrase": "wrong"}, headers={"Authorization": f"Bearer {t2}"})
    assert r.status_code == 401
