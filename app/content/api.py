from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from ..services import ModelDataService
from ..containers import AppContainer

from .models import Content, ContentIn
from .tasks import fetch_content

ROUTER = APIRouter()


@ROUTER.get("/contents", response_model=list[Content])
@inject
async def get_content_many(
    query=Depends(Provide[AppContainer.content.data.query]),
):
    return await query.all()


@ROUTER.post("/contents", response_model=Content)
@inject
async def create_content(
    content_in: ContentIn,
    query: ModelDataService = Depends(
        Provide[AppContainer.content.data.query]
    ),
):
    # -> move this to manager. APP components -> implement
    # -> wire into app
    content: Content = await query.create(content_in)
    await query.commit()
    fetch_content.delay(content.id)
    return content
