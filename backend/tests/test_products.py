def test_all(client): assert len(client.get("/api/products").json) == 6
def test_filter(client):
    r = client.get("/api/products?category=controllers").json
    assert r and all(p["category"] == "controllers" for p in r)
