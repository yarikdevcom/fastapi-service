import pytest


@pytest.mark.asyncio
async def test_simple_redis(container):
    redis = container.resources.redis()
    await redis.set("123", 100_000)
    assert int(await redis.get("123")) == 100_000
