from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from ...containers import AppContainer
from ...resources.providers import ConnectionProvider
from .models import Content, ContentIn
from .tables import CONTENT_TABLE
# from .tasks import fetch_content_async

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
    c1: ConnectionProvider = Depends(Provide[CONNECTION]),
    c2: ConnectionProvider = Depends(Provide[CONNECTION]),
):
    # test example of injecting connections
    async with connection.acquire() as cn, c1.inject(connection), c2.inject(
        connection
    ):
        assert c1.current == connection.current == cn
        assert c2.current == connection.current == cn
        content = await connection.one(
            CONTENT_TABLE.insert(content_in.dict()).returning(CONTENT_TABLE),
            # commit=True,
        )
        # if content:
        # await fetch_content_async(content["id"], connection=connection)
    return content
