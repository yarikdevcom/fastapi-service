import httpx

from celery.utils.log import get_task_logger
from dependency_injector.wiring import Provide, inject

from .providers import CELERY
from .containers import ContentContainer
from .services import ModelTableService

logger = get_task_logger(__name__)


@inject
async def fetch_content_async(
    content_id,
    query: ModelTableService = Provide[ContentContainer.query],
):
    content = await query.get(content_id)
    content.body = httpx.get(content.url).text
    await query.update(content)
    logger.info([content.id, len(content.body)])
    return None


@CELERY.task  # (autoretry_for=(Exception,))
def fetch_content(content_id: int):
    CELERY.loop.run_until_complete(fetch_content_async(content_id))
