import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from .db import create_db_and_tables
from .main import app
from .routers.problems.problems import problem_registry

PUBLIC_PAGES = ["/", "/login", "/register", "/about", "/norm"]


def make_client() -> AsyncClient:
    # `https` is required so httpx sends back the `Secure` auth cookie.
    return AsyncClient(transport=ASGITransport(app=app), base_url="https://test")


@pytest.mark.anyio
@pytest.mark.parametrize("route", PUBLIC_PAGES)
async def test_simple_read_home(route):
    async with make_client() as ac:
        response = await ac.get(route)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_simple_read_problems():
    async with make_client() as ac:
        response = await ac.get("/problems")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_simple_read_users():
    await create_db_and_tables()
    async with make_client() as ac:
        response = await ac.get("/users")
    assert response.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize("route", list(problem_registry.keys()))
async def test_problem_pages_load(route):
    async with make_client() as ac:
        response = await ac.get("/problems/" + route)
    assert response.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize("route", list(problem_registry.keys()))
async def test_problem_scoreboards_load(route):
    async with make_client() as ac:
        response = await ac.get("/problems/" + route + "-scores")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_unknown_page_renders_not_found():
    async with make_client() as ac:
        response = await ac.get("/this-page-does-not-exist")
    assert response.status_code == 200
    assert "404: Page Not Found" in response.text


@pytest.mark.anyio
async def test_me_requires_login():
    async with make_client() as ac:
        response = await ac.get("/me")
    assert response.status_code == 200
    assert "404: Page Not Found" in response.text


@pytest.mark.anyio
async def test_static_files_are_served():
    async with make_client() as ac:
        response = await ac.get("/static/output.css")
    assert response.status_code == 200


async def register_user(ac: AsyncClient, email: str, password: str, nickname: str):
    response = await ac.post(
        "/auth/register",
        json={"email": email, "password": password, "nickname": nickname},
    )
    assert response.status_code == 201
    return response


@pytest.mark.anyio
async def test_register_login_and_profile_flow():
    await create_db_and_tables()
    email = f"{uuid.uuid4()}@example.com"
    password = "test_password"
    nickname = "tester"
    async with make_client() as ac:
        await register_user(ac, email, password, nickname)

        response = await ac.post(
            "/auth/jwt/login",
            data={"username": email, "password": password},
        )
        assert response.status_code == 204

        response = await ac.get("/me")
        assert response.status_code == 200
        assert nickname in response.text

        response = await ac.get("/logout")
        assert response.status_code == 307
        assert response.headers["location"] == "/problems"

        response = await ac.get("/me")
        assert "404: Page Not Found" in response.text


@pytest.mark.anyio
async def test_duplicate_registration_is_rejected():
    await create_db_and_tables()
    email = f"{uuid.uuid4()}@example.com"
    async with make_client() as ac:
        await register_user(ac, email, "password_1", "tester_1")
        response = await ac.post(
            "/auth/register",
            json={"email": email, "password": "password_2", "nickname": "tester_2"},
        )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_login_with_bad_credentials_fails():
    await create_db_and_tables()
    email = f"{uuid.uuid4()}@example.com"
    async with make_client() as ac:
        await register_user(ac, email, "password_1", "tester_1")
        response = await ac.post(
            "/auth/jwt/login",
            data={"username": email, "password": "wrong_password"},
        )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_submit_score_updates_leaderboard():
    await create_db_and_tables()
    email = f"{uuid.uuid4()}@example.com"
    nickname = "score_submitter"
    async with make_client() as ac:
        await register_user(ac, email, "password_1", nickname)
        await ac.post(
            "/auth/jwt/login",
            data={"username": email, "password": "password_1"},
        )
        response = await ac.post(
            "/problems/collatz-submit",
            json={"submission": "100"},
        )
        assert response.status_code == 200

        response = await ac.get("/problems/collatz-scores")
        assert response.status_code == 200
        assert nickname in response.text