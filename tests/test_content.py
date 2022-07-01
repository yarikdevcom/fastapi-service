import asyncio

import pytest


@pytest.mark.asyncio
async def test_content_created(client, container):
    COUNT = 40
    URLS = [f"https://www.google.com/{i}" for i in range(COUNT)]
    responses = await asyncio.gather(
        *[client.post("/contents", json={"url": url}) for url in URLS]
    )
    for resp in responses:
        assert resp.status_code == 200

    url = URLS[0]
    response = responses[0]
    data = response.json()
    assert data["url"] == url

    responses = await asyncio.gather(
        *[client.post("/contents", json={"url": url}) for url in URLS]
    )

    query = await container.features.content.query()
    assert len(URLS) == len(list(await query.all()))

    response = await client.get("/contents")

    assert response.status_code == 200
    assert len(response.json()) == len(URLS)
