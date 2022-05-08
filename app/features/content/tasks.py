import asyncio

import httpx
from celery import shared_task
from celery.utils.log import get_task_logger
from dependency_injector.wiring import Provide, inject

from ...containers import AppContainer
from ...resources.services import ModelQueryService

logger = get_task_logger(__name__)


@inject
async def fetch_content_async(
    content_id,
    query: ModelQueryService = Provide[AppContainer.features.content.query],
):
    content = await query.get(content_id)
    content.body = httpx.get(content.url).text
    await query.update(content)
    await query.commit()
    logger.info([content.id, len(content.body)])


@shared_task(autoretry_for=(Exception,), name="fetch_content")
def fetch_content(content_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_content_async(content_id))
