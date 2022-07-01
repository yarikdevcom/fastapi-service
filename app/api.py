import asyncpg
import sqlalchemy as sa
from dependency_injector import providers
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import ORJSONResponse

from . import APP_CONTAINER

API = FastAPI(default_response_class=ORJSONResponse)

# routes
for obj in APP_CONTAINER.traverse(types=(providers.Object,)):
    api = obj()
    if isinstance(api, APIRouter):
        API.include_router(api)


# events
@API.on_event("startup")
async def on_startup():
    await APP_CONTAINER.init_resources()


@API.on_event("shutdown")
async def on_shutdown():
    await APP_CONTAINER.shutdown_resources()
    APP_CONTAINER.unwire()


# middlewares
@API.middleware("http")
async def cleanup_API_db_connections(request, call_next):
    response = await call_next(request)
    await APP_CONTAINER.resources.db.cleanup()
    return response


# exceptions
@API.exception_handler(sa.exc.TimeoutError)
@API.exception_handler(sa.exc.ResourceClosedError)
@API.exception_handler(asyncpg.exceptions.TooManyConnectionsError)
async def sa_timeout_error_exception_handler(
    request: Request, exc: sa.exc.TimeoutError
):
    return ORJSONResponse(
        status_code=500,
        content={"message": "High load on database, please try again"},
    )


@API.exception_handler(sa.exc.IntegrityError)
@API.exception_handler(sa.exc.InterfaceError)
@API.exception_handler(sa.exc.DBAPIError)
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
