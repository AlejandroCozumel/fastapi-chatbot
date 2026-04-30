import os
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
os.environ.setdefault("UPLOAD_DIR", "./data/test-uploads")

from app.main import app  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.session import engine  # noqa: E402


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    Path("./data/test-uploads").mkdir(parents=True, exist_ok=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
