from . import get_admin_token, get_customer_token
from models import Theatre

def test_new_booking_unauthorized(client):
    resp = client.post("/booking/new", json={
        "name": "The One",
        "seats": 30
    })
    assert resp.status == '401 UNAUTHORIZED'

def test_new_booking_missing_parameters(client):
    resp = client.post("/booking/new", headers={
        "Authorization": "JWT " + get_customer_token(client)
    }, json={
        "seats": 30
    })

    assert resp.status == "500 INTERNAL SERVER ERROR" # '200 OK'

def test_new_booking(client):
    theatre_name = "The One"
    resp = client.post("/booking/new", headers={
        "Authorization": "JWT " + get_customer_token(client)
    }, json={
        "name": theatre_name,
        "seats": 30
    })

    assert resp.status == '200 OK'

def test_booking_on_theatre_not_exists(client):
    Theatre.seed()
    theatre_name = "The One"
    # Theatre.theatres = list(filter(lambda theatre: theatre["name"] == theatre_name, Theatre.theatres))
    # del Theatre.table[theatre_name]
    resp = client.post("/booking/new", headers={
        "Authorization": "JWT " + get_customer_token(client)
    }, json={
        "name": theatre_name,
        "seats": 33
    })

    assert resp.status == '200 OK' and b'not exists' in resp.data

def test_booking_seat_left(client):
    theatre_name = "The One"
    resp = client.post("/theatre/new", headers={
        "Authorization": "JWT " + get_admin_token(client)
    }, json={
        "name": theatre_name,
        "seats": 30
    })

    resp = client.post("/booking/new", headers={
        "Authorization": "JWT " + get_customer_token(client)
    }, json={
        "name": theatre_name,
        "seats": 33
    })

    assert resp.status == '200 OK' and b'Sorry no seat left' in resp.data
