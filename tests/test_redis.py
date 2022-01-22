import pytest

from app.providers import REDIS


@pytest.mark.asyncio
async def test_simple_redis():
    await REDIS.set("123", 100_000)
    assert int(await REDIS.get("123")) == 100_000
