import pytest
from fastapi.testclient import TestClient

import app.auth as app_auth
from app.main import app

TEST_API_KEY = "test-api-key"


@pytest.fixture(autouse=True)
def patch_api_key(monkeypatch):
    monkeypatch.setattr(app_auth, "API_KEY", TEST_API_KEY)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {"X-API-Key": TEST_API_KEY}
