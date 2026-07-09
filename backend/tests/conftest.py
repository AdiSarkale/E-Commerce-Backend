import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient, ASGITransport

import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from main import app
from core.cache import get_redis
from utils.cache import get_cache

class FakeRedis:
    async def get(self, key):
        return None

    async def set(self, *args, **kwargs):
        return True

    async def delete(self, *args, **kwargs):
        return True

    async def ping(self):
        return True

async def override_get_redis():
    return FakeRedis()

app.dependency_overrides[get_redis] = override_get_redis

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

@pytest_asyncio.fixture(autouse=True)
def mock_email():
    with patch("services.user.send_welcome_email.delay") as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_get_cache():
    with patch(
        "utils.cache.CacheManager.get",
        new_callable=AsyncMock,
        return_value=None,
    ):
        yield

@pytest.fixture(autouse=True)
def mock_set_cache():
    with patch(
        "utils.cache.CacheManager.set",
        new_callable=AsyncMock,
        return_value=None,
    ):
        yield

@pytest.fixture(autouse=True)
def mock_delete_cache():
    with patch(
        "utils.cache.CacheManager.delete",
        new_callable=AsyncMock,
        return_value=None,
    ):
        yield
