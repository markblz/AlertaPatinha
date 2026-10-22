import os

# Before any `api.*` import: settings and the engine are built at import time.
# Tests use their own database so they never touch dev data.
_BASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+asyncpg://alertapatinha:changeme@localhost:5440/alertapatinha"
)
TEST_DB_NAME = os.environ.get("TEST_DATABASE_NAME", "alertapatinha_test")
os.environ["DATABASE_URL"] = _BASE_URL.rsplit("/", 1)[0] + "/" + TEST_DB_NAME
os.environ["ENV"] = "test"
