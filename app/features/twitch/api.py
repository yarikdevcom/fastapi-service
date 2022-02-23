from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from ...resources.services import ModelDataService
from ...containers import AppContainer

from . import API
from .models import Bot, BotIn
from .tasks import fetch_content

CONTAINER = AppContainer.features.bot


@API.get("/bots", response_model=list[Bot])
@inject
async def get_bot_many(
    query=Depends(Provide[CONTAINER.data.query])
):
    return await query.all()


@API.post("/bot", response_model=Bot)
@inject
async def create_bot(
    bot_in: BotIn,
    query: ModelDataService = Depends(Provide[CONTAINER.data.query])
):
    bot: Bot = await query.create(bot_in)
    await query.commit()
    fetch_content.delay(bot.id)
    return bot
