from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from ...containers import AppContainer
from ...resources.services import ModelQueryService
from . import API
from .containers import ContentContainer
from .models import Content, ContentIn
from .tasks import fetch_content

CONTAINER: ContentContainer = AppContainer.features.content  # type: ignore


@API.get("/contents", response_model=list[Content])
@inject
async def get_content_many(
    query=Depends(Provide[CONTAINER.query]),
):
    return await query.all()


@API.post("/contents", response_model=Content)
@inject
async def create_content(
    content_in: ContentIn,
    query: ModelQueryService = Depends(Provide[CONTAINER.query]),
):
    content: Content = await query.create(content_in)
    await query.commit()
    fetch_content.delay(content.id)
    return content
