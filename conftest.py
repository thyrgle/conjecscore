import os
import tempfile

import pytest

# In-memory SQLite creates a fresh database per pooled connection, so the
# tests could not reliably share state. Use a file-based database instead.
# `load_dotenv()` does not override variables already present in the
# environment, so CI (postgres) keeps its own DATABASE_URL.
_tempdir = tempfile.mkdtemp(prefix="conjecscore-tests-")
os.environ.setdefault(
    "DATABASE_URL", f"sqlite+aiosqlite:///{_tempdir}/test.db"
)
os.environ.setdefault("SECRET", "test-secret-that-is-long-enough-for-hs256")


@pytest.fixture(autouse=True)
def _dispose_engine():
    # anyio runs every test in a fresh event loop, but the module-global
    # engine pools asyncpg connections across tests. A connection created in
    # one loop cannot be reused in the next, so drop the whole pool after
    # each test. (aiosqlite connections run in their own thread and loop, so
    # this only matters on postgres.) The teardown runs after the test's loop
    # has closed, hence asyncio.run.
    yield
    import asyncio

    from app.db import engine

    asyncio.run(engine.dispose())