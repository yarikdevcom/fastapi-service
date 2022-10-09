import asyncio

import httpx
from celery import shared_task
from celery.utils.log import get_task_logger
from dependency_injector.wiring import Provide, inject

from ...containers import AppContainer
from ...resources.providers import ConnectionProvider
from .tables import CONTENT_TABLE

logger = get_task_logger(__name__)


@inject
async def fetch_content_async(
    content_id,
    connection: ConnectionProvider = Provide[
        AppContainer.resources.db.connection
    ],
):
    async with connection.acquire():
        content = await connection.one(
            CONTENT_TABLE.select(CONTENT_TABLE.c.id == content_id)
        )
        async with httpx.AsyncClient() as cl:
            body = (await cl.get(content["url"])).text
        await connection.execute(
            CONTENT_TABLE.update(CONTENT_TABLE.c.id == content_id).values(
                {"body": body}
            ),
        )


@shared_task(autoretry_for=(Exception,), name="fetch_content")
def fetch_content(content_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_content_async(content_id))
