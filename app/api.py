from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from .containers import ContentContainer
from .models import Content, ContentIn
from .tasks import fetch_content

router = APIRouter()


@router.get("/contents", response_model=list[Content])
@inject
async def get_content_many(
    query=Depends(Provide(ContentContainer.query)),
):
    return await query.all()


@router.post("/contents", response_model=Content)
@inject
async def create_content(
    content_in: ContentIn,
    query=Depends(Provide(ContentContainer.query)),
):
    content: Content = await query.create(content_in)
    await query.db.connection.commit()
    fetch_content.delay(content.id)
    return content
