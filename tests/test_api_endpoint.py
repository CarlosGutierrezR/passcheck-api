# tests/test_api_endpoint.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_check_endpoint_ok():
    resp = client.post("/check", json={"password": "password"})
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == {"pwned", "count"}
    assert isinstance(data["pwned"], bool)
    assert isinstance(data["count"], int)
