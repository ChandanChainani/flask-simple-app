from . import get_admin_token
from models import Theatre

def test_get_theatres(client):
    data = client.get("/theatres").get_json()
    theatres = {
        "data": Theatre.get()
    }
    assert data == theatres

def test_get_theatre(client):
    theatre_name = "PVR Cinemas"
    theatre = Theatre.get(theatre_name)
    theatres = { "data": theatre }
    data = client.get("/theatres/" + theatre_name).get_json()
    assert data == theatres
    assert theatre['seats'] == data['data']['seats']

def test_theatre_not_found(client):
    theatre_name = "The One"
    data = client.get("/theatres/" + theatre_name).get_json()
    message = {
        "message": "Not found"
    }
    assert data == message

def test_add_theatre_unauthorized(client):
    resp = client.post("/theatre/new", json={
        "name": "The One",
        "seats": 30
    })
    assert resp.status == '401 UNAUTHORIZED'

def test_add_theatre(client):
    theatre_name = "The One"
    resp = client.post("/theatre/new", headers={
        "Authorization": "JWT " + get_admin_token(client)
    }, json={
        "name": theatre_name,
        "seats": 30
    })

    resp2 = client.get("/theatres/" + theatre_name)

    assert resp.status == '201 CREATED'
    assert resp2.status == '200 OK' and bytes(theatre_name, 'utf8') in resp2.data
