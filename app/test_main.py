from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

@app.get("/")
def test_simple_read_home():
    response = client.get("/")
    assert response.status_code == 200

