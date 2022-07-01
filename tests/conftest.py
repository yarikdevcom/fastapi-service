import pytest_asyncio
from httpx import AsyncClient

from app import APP_CONTAINER
from app.api import API


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=API, base_url="http://test.com") as cl:
        yield cl


@pytest_asyncio.fixture
async def container():
    await APP_CONTAINER.init_resources()
    yield APP_CONTAINER
    await APP_CONTAINER.shutdown_resources()
