import pytest
import pytest_asyncio

from httpx import AsyncClient

from app import __version__
from app.main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test.com") as cl:
        yield cl


@pytest.mark.asyncio
async def test_root_url(client):
    response = await client.get("/")
    assert response.status_code == 200


def test_version():
    assert __version__ == "0.1.0"
