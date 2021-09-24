from . import login

def test_auth_admin(client):
    resp = login(client, "user1", "u1")
    assert resp.status == '200 OK' and b'access_token' in resp.data

def test_auth_customer(client):
    resp = login(client, "user2", "u2")
    assert resp.status == '200 OK' and b'access_token' in resp.data
