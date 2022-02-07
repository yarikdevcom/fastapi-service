from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from .containers import ChannelContainer
from .models import Channel, ChannelIn
from .tasks import get_web_page

router = APIRouter()


@router.get("/channels", response_model=list[Channel])
@inject
async def get_channel_many(query=Depends(Provide(ChannelContainer.query))):
    for i in range(60):
        get_web_page.delay("https://www.google.com/")
    return await query.all()


@router.post("/channels", response_model=Channel)
@inject
async def create_channel(
    channel: ChannelIn, query=Depends(Provide(ChannelContainer.query))
):
    return await query.create(channel)


@router.get("/getgoogle")
async def get_google_in_bg():
    for _ in range(60):
        get_web_page.delay("https://www.google.com")
