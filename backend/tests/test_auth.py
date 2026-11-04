def test_register_login(client):
    d = {"name": "A", "email": "a@b.co", "password": "secret1"}
    assert client.post("/api/auth/register", json=d).status_code == 201
    assert client.post("/api/auth/login", json=d).status_code == 200
    assert client.post("/api/auth/login", json={**d, "password": "no"}).status_code == 401
