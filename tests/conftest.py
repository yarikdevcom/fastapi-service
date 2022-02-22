import pytest_asyncio

from httpx import AsyncClient
from fastapi import APIRouter
from sqlalchemy.exc import ResourceClosedError

from app import APP, APP_CONTAINER

test_router = APIRouter()


@test_router.get("/raise404")
async def get_bot_many():
    raise ResourceClosedError


@pytest_asyncio.fixture
async def client():
    APP.include_router(test_router)
    async_cl = AsyncClient(app=APP, base_url="http://test.com")
    async with async_cl as cl:
        yield cl


@pytest_asyncio.fixture
async def container():
    await APP_CONTAINER.init_resources()
    yield APP_CONTAINER
    await APP_CONTAINER.shutdown_resources()
