import asyncio

import asyncpg
import sqlalchemy as sa
from celery.signals import task_postrun, task_prerun
from dependency_injector import providers
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import ORJSONResponse

from .containers import AppContainer

__version__ = "0.1.0"


APP = FastAPI(default_response_class=ORJSONResponse)

# containers
APP_CONTAINER = AppContainer()
APP_CONTAINER.config.from_yaml("./configs/test.yml")
APP_CONTAINER.check_dependencies()
APP_CONTAINER.resources.celery()

# routes
for obj in APP_CONTAINER.traverse(types=(providers.Object,)):
    api = obj()
    if isinstance(api, APIRouter):
        APP.include_router(api)


# events
@APP.on_event("startup")
async def on_startup():
    await APP_CONTAINER.init_resources()


@APP.on_event("shutdown")
async def on_shutdown():
    await APP_CONTAINER.shutdown_resources()
    APP_CONTAINER.unwire()


# middlewares
@APP.middleware("http")
async def cleanup_app_db_connections(request, call_next):
    response = await call_next(request)
    await APP_CONTAINER.resources.db.cleanup()
    return response


# exceptions
@APP.exception_handler(sa.exc.TimeoutError)
@APP.exception_handler(sa.exc.ResourceClosedError)
@APP.exception_handler(asyncpg.exceptions.TooManyConnectionsError)
async def sa_timeout_error_exception_handler(
    request: Request, exc: sa.exc.TimeoutError
):
    return ORJSONResponse(
        status_code=500,
        content={"message": "High load on database, please try again"},
    )


@APP.exception_handler(sa.exc.IntegrityError)
@APP.exception_handler(sa.exc.InterfaceError)
@APP.exception_handler(sa.exc.DBAPIError)
async def sa_integrity_error_exception_handler(
    request: Request, exc: sa.exc.IntegrityError
):
    orig = str(exc.orig)
    if "asyncpg.exceptions.UniqueViolationError" in orig:
        message = f"Database unique value violation: {orig.split('>: ')[1]}"
        return ORJSONResponse(status_code=409, content={"message": message})

    return ORJSONResponse(
        status_code=500, content={"message": f"Database error: {exc}"}
    )


@task_prerun.connect
def on_celery_task_pre_run(**kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(APP_CONTAINER.init_resources())


@task_postrun.connect
def on_celery_task_post_run(**kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(APP_CONTAINER.shutdown_resources())
