import os
import tempfile

# In-memory SQLite creates a fresh database per pooled connection, so the
# tests could not reliably share state. Use a file-based database instead.
# `load_dotenv()` does not override variables already present in the
# environment, so CI (postgres) keeps its own DATABASE_URL.
_tempdir = tempfile.mkdtemp(prefix="conjecscore-tests-")
os.environ.setdefault(
    "DATABASE_URL", f"sqlite+aiosqlite:///{_tempdir}/test.db"
)
os.environ.setdefault("SECRET", "test-secret-that-is-long-enough-for-hs256")