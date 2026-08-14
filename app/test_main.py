import pytest
from httpx import ASGITransport, AsyncClient

from .main import app
from .db import create_db_and_tables


@pytest.mark.anyio
async def test_simple_read_home():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_simple_read_problems():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/problems")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_simple_read_login():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/login")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_simple_read_register():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/register")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_simple_read_users():
    await create_db_and_tables()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/users") 
    assert response.status_code == 200
