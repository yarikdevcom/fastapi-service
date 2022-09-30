import asyncio

import pytest

from app.features.content.tables import CONTENT_TABLE


@pytest.mark.asyncio
async def test_content_created(client, cursor):
    COUNT = 1000

    URLS = [f"https://www.google.com/{i}" for i in range(COUNT)]
    responses = await asyncio.gather(
        *[client.post("/contents", json={"url": url}) for url in URLS]
    )
    for resp in responses:
        assert resp.status_code == 200, resp.json()

    url = URLS[0]
    response = responses[0]
    data = response.json()
    assert data["url"] == url

    responses = await asyncio.gather(
        *[client.post("/contents", json={"url": url}) for url in URLS]
    )
    for resp in responses:
        assert resp.status_code == 409, resp.json()

    assert len(URLS) == len(list(await cursor.many(CONTENT_TABLE.select())))
