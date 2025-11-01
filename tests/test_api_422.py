# tests/test_api_422.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_check_missing_field():
    # Falta el campo "password"
    resp = client.post("/check", json={})
    assert resp.status_code == 422

def test_check_empty_password():
    # Cadena vacía no cumple min_length=1
    resp = client.post("/check", json={"password": ""})
    assert resp.status_code == 422
