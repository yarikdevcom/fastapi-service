import pytest
import asyncio
import random
import sqlalchemy as sa

from app.models import Bot

'''Tests must be run together'''


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_create_delete(client, container):
    create_one = await client.post("/bot", json={"secret_id": "sercret123",
                        "client_id": "client123", "nickname": "Cooper123"})
    assert create_one.status_code == 200

    query = await container.bot.query()
    id = create_one.json()["id"]
    await query.delete(id_=id)
    await query.commit()

    query = await container.bot.query()
    deleted_bot = await query.get(id)
    assert deleted_bot is None

    create_many = await asyncio.gather(
        *[client.post("/bot", json={"secret_id": "sercret123", "client_id":
                                    "client123", "nickname": "to_filter"})
        for _ in range(10)]
    )
    for item in create_many:
        assert item.status_code == 200


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_filter(container):

    query = await container.bot.query()
    filtered_bots = await query.filter(
        query.table.c.nickname == "to_filter"
    )
    assert len(list(filtered_bots)) >= 10


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_update(container):
    query = await container.bot.query()
    bots = list(await query.filter(
        query.table.c.nickname == "to_filter"
    ))
    print(bots)

    for bot in bots:
        query = await container.bot.query()
        bot = bot.dict()
        id = bot["id"]
        secret_id = bot["secret_id"]
        client_id = bot["client_id"]
        nickname = bot["nickname"]
        load = random.randint(0, 40)
        max_load = bot["max_load"]
        updated_bot = Bot(
            id=id, secret_id=secret_id, client_id=client_id,
            nickname=nickname, load=load, max_load=max_load
        )
        await query.update(updated_bot)
        await query.commit()

    query = await container.bot.query()
    filtered_bots = await query.filter(
        query=sa.and_(
            query.table.c.nickname == "to_filter",
            sa.not_(query.table.c.load == 0)
            )
    )
    assert len(list(filtered_bots)) >= 10

    for bot in bots:
        query = await container.bot.query()
        id = bot.dict()["id"]
        print(id)
        await query.delete(id_=id)
        await query.commit()
