def test_order_flow(client):
    client.post("/api/auth/register", json={"email": "a@b.co", "password": "secret1"})
    client.post("/api/cart", json={"product_id": 1, "quantity": 2})
    r = client.post("/api/orders")
    assert r.status_code == 201 and r.json["total"] == 398
