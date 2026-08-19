import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Generator

import httpx
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SECRET = "test-secret-that-is-long-enough-for-hs256"


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="session")
def base_url(tmp_path_factory) -> Generator[str, None, None]:
    """Start the app behind a TLS server with a self-signed certificate."""
    workdir = tmp_path_factory.mktemp("server")
    keyfile = workdir / "key.pem"
    certfile = workdir / "cert.pem"
    subprocess.run(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", str(keyfile), "-out", str(certfile),
            "-days", "1", "-nodes", "-subj", "/CN=localhost",
        ],
        check=True,
        capture_output=True,
    )
    port = _free_port()
    env = {
        **os.environ,
        "DATABASE_URL": f"sqlite+aiosqlite:///{workdir / 'test.db'}",
        "SECRET": SECRET,
    }
    server_log = workdir / "server.log"
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn", "app.main:app",
            "--host", "127.0.0.1", "--port", str(port),
            "--ssl-keyfile", str(keyfile), "--ssl-certfile", str(certfile),
            "--log-level", "warning",
        ],
        cwd=REPO_ROOT,
        env=env,
        stdout=server_log.open("w"),
        stderr=subprocess.STDOUT,
    )
    url = f"https://127.0.0.1:{port}"
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            try:
                response = httpx.get(url + "/", verify=False, timeout=2)
                if response.status_code == 200:
                    break
            except httpx.HTTPError:
                time.sleep(0.25)
        else:
            raise RuntimeError(
                "test server did not become ready:\n"
                + server_log.read_text()
            )
        yield url
    finally:
        proc.terminate()
        proc.wait(timeout=10)


# The sync Playwright driver keeps an asyncio event loop running in the main
# thread, which clashes with the anyio-based tests in app/test_main.py. Keep
# the driver and browser scoped to each test so no loop is left running
# around the other tests.
@pytest.fixture
def playwright() -> Generator[Playwright, None, None]:
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture
def browser(playwright: Playwright) -> Generator[Browser, None, None]:
    browser = playwright.chromium.launch()
    yield browser
    browser.close()


@pytest.fixture
def browser_context_args() -> dict:
    # The auth cookie is `Secure`, so the test server runs TLS with a
    # self-signed certificate. Ignore the certificate errors this produces.
    return {"ignore_https_errors": True}


@pytest.fixture
def context(
    browser: Browser, browser_context_args: dict
) -> Generator[BrowserContext, None, None]:
    ctx = browser.new_context(**browser_context_args)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    p = context.new_page()
    yield p
    p.close()