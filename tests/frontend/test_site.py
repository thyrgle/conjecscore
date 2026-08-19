import json
import uuid
from pathlib import Path

from playwright.sync_api import Page, expect


def register_and_login(page: Page, base_url: str) -> tuple[str, str]:
    """Register a fresh account and log in through the UI."""
    nickname = "e2e_" + uuid.uuid4().hex[:8]
    email = f"{uuid.uuid4()}@example.com"
    password = "test_password_123"

    page.goto(base_url + "/register")
    page.fill("#email", email)
    page.fill("#nickname", nickname)
    page.fill("#password", password)
    page.click("#submit")
    page.wait_for_url("**/login")

    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#submit")
    page.wait_for_url("**/problems")
    return nickname, email


def test_homepage_loads(page: Page, base_url: str):
    page.goto(base_url + "/")
    expect(page).to_have_title("conjecscore")
    expect(page.get_by_role("heading", level=1)).to_have_text("conjecscore")
    expect(page.get_by_text("Mathematical competitions for solving the unsolved.")).to_be_visible()
    expect(page.get_by_role("link", name="Problems")).to_be_visible()
    expect(page.get_by_role("link", name="About")).to_be_visible()
    expect(page.get_by_role("link", name="Login")).to_be_visible()
    expect(page.get_by_role("link", name="Sign up")).to_be_visible()


def test_navigation_from_home_to_problem_page(page: Page, base_url: str):
    page.goto(base_url + "/")
    page.get_by_role("link", name="Problems").click()
    page.wait_for_url("**/problems")
    expect(page.get_by_role("heading", name="Problems")).to_be_visible()
    expect(page.get_by_role("heading", name="Collatz Orbits")).to_be_visible()

    page.get_by_role("heading", name="Collatz Orbits").click()
    page.wait_for_url("**/problems/collatz")
    expect(page).to_have_title("Collatz Orbits")
    expect(page.get_by_role("heading", name="Leaderboard")).to_be_visible()
    expect(page.locator("#submission")).to_be_visible()


def test_login_with_bad_credentials_shows_error(page: Page, base_url: str):
    page.goto(base_url + "/login")
    page.fill("#email", "nobody@example.com")
    page.fill("#password", "wrong_password")
    page.click("#submit")
    expect(page.locator("#loginstatus")).to_have_text(
        "Invalid username or password."
    )


def test_register_login_profile_and_logout_flow(page: Page, base_url: str):
    nickname, _ = register_and_login(page, base_url)

    expect(page.get_by_role("link", name=nickname)).to_be_visible()
    expect(page.get_by_role("link", name="Logout")).to_be_visible()

    page.goto(base_url + "/me")
    expect(page).to_have_title(nickname)
    expect(page.get_by_role("heading", name=nickname)).to_be_visible()
    expect(page.get_by_text("Cumulative Score")).to_be_visible()
    expect(page.get_by_text("What is this?")).to_be_visible()

    page.get_by_role("link", name="Logout").click()
    page.wait_for_url("**/problems")
    expect(page.get_by_role("link", name="Login")).to_be_visible()
    expect(page.get_by_role("link", name="Sign up")).to_be_visible()


def test_submit_score_updates_leaderboard(page: Page, base_url: str):
    nickname, _ = register_and_login(page, base_url)

    page.goto(base_url + "/problems/collatz")
    page.fill("#submission", "27")
    with page.expect_response(
        lambda r: r.request.method == "POST" and "collatz-submit" in r.url
    ):
        page.click('input[type="submit"]')
    expect(page.locator("#status")).to_have_text("You scored 8200.")

    page.reload()
    expect(page.locator("#leaderboard")).to_contain_text(nickname)
    expect(page.locator("#leaderboard")).to_contain_text("8200")


def test_json_file_submission_and_variant_switch(page: Page, base_url: str, tmp_path: Path):
    # The problem pages fetch MathJax/highlight.js from CDNs; the submission
    # itself only needs the score modules served by the app itself.
    register_and_login(page, base_url)

    page.goto(base_url + "/problems/conway")
    expect(page).to_have_title("Conway's 99 Problem")
    expect(page.locator("#variant-select")).to_be_visible()

    graph = {str(i): [] for i in range(99)}
    graph_file = tmp_path / "graph.json"
    graph_file.write_text(json.dumps(graph))
    with page.expect_response(
        lambda r: r.request.method == "POST" and "conway-submit" in r.url
    ):
        page.set_input_files("#submission", graph_file)
        page.click('input[type="submit"]')
    expect(page.locator("#status")).to_have_text("You scored 19404.")

    # Switching variants refetches the leaderboard for the new variant.
    with page.expect_response(
        lambda r: "conway-scores" in r.url and "variant=6273" in r.url
    ):
        page.select_option("#variant-select", label="n = 6273")