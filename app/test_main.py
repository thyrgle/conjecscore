import pytest
from fastapi.testclient import TestClient

from .main import app
from .db import create_db_and_tables

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

@pytest.mark.asyncio(loop_scope="session")
async def test_simple_read_users():
    await create_db_and_tables()
    response = client.get("/users")
    assert response.status_code == 200

