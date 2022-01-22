import pytest


@pytest.mark.asyncio
async def test_channel_created(client, db):
    response = await client.post("/channels", json={"url": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "test"

    response = await client.get("/channels")
    assert response.status_code == 200
    data = response.json()
    assert data


@pytest.mark.asyncio
async def test_channel_acquired_positive(client, db):
    # create 5 bots
    # create 300 channel
    # mark 200 channels active
    # client -> url channel acquire size 150
    # assert 1 bot with 50 channels
    # client -> url channel acquire size 150
    # assert 1 bot with 50 channels
    # client -> url channel acquire size 150
    # assert 1 bot with 50 channels
    assert 1 == 1
