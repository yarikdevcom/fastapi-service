import asyncio

import pytest


@pytest.mark.asyncio
async def test_content_created(client):
    url = "https://www.google.com/"
    response = await client.post("/contents", json={"url": url})
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == url

    await asyncio.sleep(2)

    response = await client.get("/contents")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data
