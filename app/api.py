from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from .containers import ChannelContainer
from .models import Channel, ChannelIn

router = APIRouter()


@router.get("/channels", response_model=list[Channel])
@inject
async def get_channel_many(query=Depends(Provide(ChannelContainer.query))):
    return await query.all()


@router.post("/channels", response_model=Channel)
@inject
async def create_channel(
    channel: ChannelIn, query=Depends(Provide(ChannelContainer.query))
):
    return await query.create(channel)
