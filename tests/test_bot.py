import pytest
import asyncio
import random
import sqlalchemy as sa

from app.features.twitch.models import BotIn, Bot
'''Tests must be run together'''

# @pytest.fixture()
# async def delete


@pytest.mark.asyncio
async def test_create_delete(client, container):
    create_one = await client.post("/bot", json={"secret_id": "sercret123",
                        "client_id": "client123", "nickname": "Cooper123"})
    assert create_one.status_code == 200

    query = await container.features.bot.data.query()
    id = create_one.json()["id"]
    await query.delete(id_=id)
    await query.commit()

    query = await container.features.bot.data.query()
    deleted_bot = await query.get(id)
    assert deleted_bot is None

    create_many = await asyncio.gather(
        *[client.post("/bot", json={"secret_id": "sercret123", "client_id":
                                    "client123", "nickname": "to_filter"})
        for _ in range(10)]
    )
    query = await container.features.bot.data.query()
    for item in create_many:
        assert item.status_code == 200
        item_json = item.json()

        id = item_json["id"]
        item_from_db = await query.get(id)
        assert item_from_db.dict() == item_json

        await query.delete(id_=id)
    await query.commit()


@pytest.mark.asyncio
async def test_filter(client, container):
    to_filter = await asyncio.gather(
        *[client.post("/bot", json={"secret_id": "sercret123", "client_id":
                                    "client123", "nickname": "to_filter"})
        for _ in range(10)]
    )

    query = await container.features.bot.data.query()
    filtered_bots = await query.filter(
        query.table.c.nickname == "to_filter"
    )
    assert len(list(filtered_bots)) >= 10

    for item in to_filter:
        id = item.json()["id"]
        await query.delete(id_=id)
    await query.commit()


@pytest.mark.asyncio
async def test_update(client, container):
    await asyncio.gather(
        *[client.post("/bot", json={"secret_id": "sercret123", "client_id":
                                    "client123", "nickname": "to_filter"})
        for _ in range(10)]
    )
    query = await container.features.bot.data.query()
    bots = list(await query.filter(
        query.table.c.nickname == "to_filter"
    ))

    for bot in bots:
        bot = bot.dict()
        id = bot["id"]
        secret_id = bot["secret_id"]
        client_id = bot["client_id"]
        nickname = bot["nickname"]
        load = random.randint(1, 40)
        max_load = bot["max_load"]
        updated_bot = Bot(
            id=id, secret_id=secret_id, client_id=client_id,
            nickname=nickname, load=load, max_load=max_load
        )
        await query.update(updated_bot)
    await query.commit()

    query = await container.features.bot.data.query()
    filtered_bots = await query.filter(
        query=sa.and_(
            query.table.c.nickname == "to_filter",
            sa.not_(query.table.c.load == 0)
            )
    )
    assert len(list(filtered_bots)) >= 10

    for bot in bots:
        id = bot.dict()["id"]
        await query.delete(id_=id)
    await query.commit()

    query = await container.features.bot.data.query()
    check_for_delete = await query.filter(
        query=sa.and_(
            query.table.c.nickname == "to_filter",
            sa.not_(query.table.c.load == 0)
            )
    )
    assert len(list(check_for_delete)) == 0


@pytest.mark.asyncio
async def test_rollback(client, container):
    query = await container.features.bot.data.query()
    
    bot_1 = BotIn(
        secret_id ='test_raise1',
        client_id='test',
        nickname='testn',
        load=4
    )
    bot_2 = BotIn(
        secret_id ='test_raise2',
        client_id='test',
        nickname='testn',
        load=4
    )

    create_1 = await query.create(bot_1)
    create_2 = await query.create(bot_2)
    assert create_1 is not None
    assert create_2 is not None

    await client.get('/raise404')
    await query.commit()

    query = await container.features.bot.data.query()
    check_bot_1 = await query.filter(
        query=(query.table.c.secret_id == "test_raise1")
    )
    check_bot_2 = await query.filter(
        query=(query.table.c.secret_id == "test_raise2")
    )
    assert list(check_bot_1) == []
    assert list(check_bot_2) == []
