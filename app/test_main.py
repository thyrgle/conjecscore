from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_simple_read_home():
    response = client.get("/")
    assert response.status_code == 200

def test_simple_read_problems():
    response = client.get("/problems")
    assert response.status_code == 200

def test_simple_read_login():
    response = client.get("/login")
    assert response.status_code == 200

def test_simple_read_register():
    response = client.get("/register")
    assert response.status_code == 200
