import asyncio

from celery.signals import worker_init, worker_shutdown

from . import APP_CONTAINER

APP_CONTAINER.resources.celery()


@worker_init.connect
def on_celery_task_pre_run(**_):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(APP_CONTAINER.init_resources())


@worker_shutdown.connect
def on_celery_task_post_run(**_):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(APP_CONTAINER.shutdown_resources())
