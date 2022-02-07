import httpx

from celery.utils.log import get_task_logger

from .providers import CELERY

logger = get_task_logger(__name__)


@CELERY.task
def get_web_page(url):
    response = httpx.get(url)
    logger.info([url, len(response.text)])
