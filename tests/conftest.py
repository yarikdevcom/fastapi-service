import pytest_asyncio

from httpx import AsyncClient

from app import APP, APP_CONTAINER


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=APP, base_url="http://test.com") as cl:
        yield cl


@pytest_asyncio.fixture
async def container():
    await APP_CONTAINER.init_resources()
    yield APP_CONTAINER
    await APP_CONTAINER.shutdown_resources()
