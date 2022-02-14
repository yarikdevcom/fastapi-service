import pytest
import asyncio
import random
import sqlalchemy as sa

from app.models import Bot


@pytest.mark.asyncio
async def test_bot(client, container):
    query = await container.bot.query()
    bots_before = list(await query.all())
    created_bot = await client.post("/bot", json={"secret_id": "sercret123",
                            "client_id": "client123", "nickname": "Cooper123"})
    assert created_bot.status_code == 200

    query = await container.bot.query()
    bots_after = list(await query.all())
    assert len(bots_before) + 1 == len(bots_after)

    query = await container.bot.query()
    id = created_bot.json()["id"]
    await query.delete(id_=id)

    query = await container.bot.query()
    deleted_bot = await query.get(id)
    assert deleted_bot is None

    bots = await asyncio.gather(
        *[client.post("/bot", json={"secret_id": "sercret123", "client_id": "client123", "nickname": "to_filter"})
        for _ in range(10)]
    )

    for bot in bots:
        assert bot.status_code == 200

    query = await container.bot.query()
    filtered_bots = await query.filter(
        query.table.c.nickname == "to_filter"
    )
    assert len(list(filtered_bots)) >= 10

    for bot in bots:
        query = await container.bot.query()
        bot = bot.json()
        id = bot["id"]
        secret_id = bot["secret_id"]
        client_id = bot["client_id"]
        nickname = bot["nickname"]
        load = random.randint(0, 40)
        max_load = bot["max_load"]
        updated_bot = Bot(
            id=id, secret_id=secret_id, client_id=client_id, nickname=nickname, load=load, max_load=max_load
        )
        await query.update(updated_bot)

    query = await container.bot.query()
    filtered_load = await query.filter(
        query=sa.and_(
            query.table.c.nickname == "to_filter",
            sa.not_(query.table.c.load == 0)
            )
    )
    assert len(list(filtered_load)) >= 10

    for bot in bots:
        query = await container.bot.query()
        id = bot.json()["id"]
        await query.delete(id_=id)
