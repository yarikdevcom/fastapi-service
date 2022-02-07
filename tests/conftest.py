import pytest_asyncio

from httpx import AsyncClient

from app import APP

import pytest
import asyncio


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=APP, base_url="http://test.com") as cl:
        yield cl


@pytest.fixture(scope="session")
def event_loop():
    # NOTE: https://github.com/pytest-dev/
    # pytest-asyncio/issues/207#issuecomment-943474080
    # absolute sh*t for pytest_asyncio loops
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
