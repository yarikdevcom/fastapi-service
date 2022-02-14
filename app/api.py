from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from app.services import ModelQueryService

from .containers import AppContainer
from .models import Content, ContentIn, Bot, BotIn

from .tasks import fetch_content

router = APIRouter()


@router.get("/contents", response_model=list[Content])
@inject
async def get_content_many(
    query=Depends(Provide[AppContainer.content.query]),
):
    return await query.all()


@router.get("/bots", response_model=list[Bot])
@inject
async def get_bot_many(
    query=Depends(Provide[AppContainer.bot.query])
):
    return await query.all()


@router.post("/bot", response_model=Bot)
@inject
async def create_bot(
    bot_in: BotIn,
    query: ModelQueryService = Depends(Provide[AppContainer.bot.query])
):
    bot: Bot = await query.create(bot_in)
    await query.commit()
    fetch_content.delay(bot.id)
    return bot


@router.post("/contents", response_model=Content)
@inject
async def create_content(
    content_in: ContentIn,
    query: ModelQueryService = Depends(Provide[AppContainer.content.query]),
):
    # -> move this to manager. APP components -> implement
    # -> wire into app
    content: Content = await query.create(content_in)
    await query.commit()
    fetch_content.delay(content.id)
    return content
