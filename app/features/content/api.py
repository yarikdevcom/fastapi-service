from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from ...containers import AppContainer
from ...resources.providers import ConnectionProvider
from .models import Content, ContentIn
from .tables import CONTENT_TABLE
from .tasks import fetch_content

CONNECTION = AppContainer.resources.db.connection  # type: ignore
API = APIRouter()


@API.get("/contents", response_model=list[Content])
@inject
async def get_content_many(
    connection: ConnectionProvider = Depends(Provide[CONNECTION]),
):
    return await connection.many(CONTENT_TABLE.select())


@API.post("/contents", response_model=Content)
@inject
async def create_content(
    content_in: ContentIn,
    connection: ConnectionProvider = Depends(Provide[CONNECTION]),
):
    content = await connection.one(
        CONTENT_TABLE.insert(content_in.dict()).returning(CONTENT_TABLE),
        commit=True,
    )
    fetch_content.apply_async((content["id"],))
    return content
