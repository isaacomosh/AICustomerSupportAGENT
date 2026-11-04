def _register(client):
    client.post("/api/auth/register", json={"email": "a@b.co", "password": "secret1"})

def test_chat_uses_rag(client, monkeypatch):
    from app.services import chatbot_service as s
    monkeypatch.setattr(s, "retrieve", lambda q: ["[delivery] Standard takes 3-5 days"])
    monkeypatch.setattr(s, "generate", lambda q, c, h, lang="en", toolbox=None: "3-5 days" if c else "?")
    assert client.post("/api/chat", json={"message": "delivery time?", "lang": "sw"}).json["reply"] == "3-5 days"
    assert client.post("/api/chat", json={"message": ""}).status_code == 400

def _fake_model(monkeypatch, name="horizon vr one", qty=2):
    from app.services import chatbot_service as s
    monkeypatch.setattr(s, "retrieve", lambda q: [])
    def fake(q, c, h, lang="en", toolbox=None):
        toolbox.run("draft_order", {"items": [{"product_name": name, "quantity": qty}]}); return "Please confirm"
    monkeypatch.setattr(s, "generate", fake)

def test_order_by_chat_needs_confirmation(client, monkeypatch):
    _fake_model(monkeypatch); _register(client)
    r = client.post("/api/chat", json={"message": "nipe VR mbili"}).json
    assert r["action"]["type"] == "confirm_order" and r["action"]["total"] == 898
    assert client.get("/api/orders").json == []              # drafting alone places nothing
    assert client.post("/api/chat/confirm-order").status_code == 201
    assert client.post("/api/chat/confirm-order").status_code == 400   # draft is single-use

def test_order_tool_requires_login(client, monkeypatch):
    _fake_model(monkeypatch)
    assert client.post("/api/chat", json={"message": "order a VR"}).json["action"]["type"] == "login"

def test_order_tool_rejects_out_of_stock(client, monkeypatch):
    _fake_model(monkeypatch, name="Horizon VR Air", qty=1); _register(client)
    assert client.post("/api/chat", json={"message": "order"}).json["action"] is None
