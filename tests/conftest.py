import pytest_asyncio
from httpx import AsyncClient

from app import APP_CONTAINER
from app.api import API

# TODO: we need a specific requirements
# so all installments will be testing -> running service
# we ensure we will have full API test with all errors could
# happen


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(app=API, base_url="http://test.com") as cl:
        yield cl


@pytest_asyncio.fixture
async def postgresql():
    pass


@pytest_asyncio.fixture
async def redis():
    pass


@pytest_asyncio.fixture
async def app(postgresql, redis):
    # start container

    await APP_CONTAINER.init_resources()
    yield APP_CONTAINER

    # TODO: auto create and clear db with migration
    await APP_CONTAINER.shutdown_resources()


@pytest_asyncio.fixture
async def cursor(app):
    return await app.resources.db.connection()
