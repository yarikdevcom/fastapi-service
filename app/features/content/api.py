from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from ...resources.services import ModelDataService
from ...containers import AppContainer

from . import API
from .models import Content, ContentIn
from .tasks import fetch_content

CONTAINER = AppContainer.features.content


@API.get("/contents", response_model=list[Content])
@inject
async def get_content_many(
    query=Depends(Provide[CONTAINER.data.query]),
):
    return await query.all()


@API.post("/contents", response_model=Content)
@inject
async def create_content(
    content_in: ContentIn,
    query: ModelDataService = Depends(Provide[CONTAINER.data.query]),
):
    content: Content = await query.create(content_in)
    await query.commit()
    fetch_content.delay(content.id)
    return content
