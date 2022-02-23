from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from ...resources.services import ModelDataService
from ...containers import AppContainer

from . import API
from .models import Bot, BotIn, Channel, ChannelIn

CONTAINER = AppContainer.features.twitch


@API.get("/bots", response_model=list[Bot])
@inject
async def get_bot_many(
    query=Depends(Provide[CONTAINER.bot.query])
):
    return await query.all()


@API.post("/bot", response_model=Bot)
@inject
async def create_bot(
    bot_in: BotIn,
    query: ModelDataService = Depends(Provide[CONTAINER.bot.query])
):
    bot: Bot = await query.create(bot_in)
    await query.commit()
    return bot


@API.get("/channels", response_model=list[Channel])
@inject
async def get_channel_many(
    query=Depends(Provide[CONTAINER.channel.query])
):
    return await query.all()


@API.post("/channel", response_model=Channel)
@inject
async def create_channel(
    channel_in: ChannelIn,
    query: ModelDataService = Depends(Provide[CONTAINER.channel.query])
):
    channel: Channel = await query.create(channel_in)
    await query.commit()
    return channel
