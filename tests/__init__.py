def login(client, username, password):
    return client.post("/auth", json={
        "username": username,
        "password": password,
    })

def get_token(client, username, password):
    data = login(client, username, password).get_json()
    return data['access_token']

def get_admin_token(client):
    return get_token(client, "user1", "u1")

def get_customer_token(client):
    return get_token(client, "user2", "u2")
