import importlib

import asyncpg
import sqlalchemy as sa
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from . import APP_CONTAINER

API = FastAPI(default_response_class=ORJSONResponse)

for package in APP_CONTAINER.wiring_config.packages:
    api_module = importlib.import_module(f"{package}.api", package=__package__)
    API.include_router(api_module.API)


API.add_middleware(
    CORSMiddleware,
    allow_origins=APP_CONTAINER.config.api.cors.allow_origins(),
    allow_credentials=APP_CONTAINER.config.api.cors.allow_credentials(),
    allow_methods=APP_CONTAINER.config.api.cors.allow_methods(),
    allow_headers=APP_CONTAINER.config.api.cors.allow_headers(),
    expose_headers=APP_CONTAINER.config.api.cors.expose_headers(),
)


# events
@API.on_event("startup")
async def on_startup():
    await APP_CONTAINER.init_resources()


@API.on_event("shutdown")
async def on_shutdown():
    await APP_CONTAINER.shutdown_resources()
    APP_CONTAINER.unwire()


# exceptions
@API.exception_handler(sa.exc.TimeoutError)
@API.exception_handler(asyncpg.exceptions.TooManyConnectionsError)
async def sa_timeout_error_exception_handler(
    request: Request, exc: sa.exc.TimeoutError
):
    return ORJSONResponse(
        status_code=500,
        content={"message": "High load on database, please try again"},
    )


@API.exception_handler(asyncpg.exceptions.UniqueViolationError)
@API.exception_handler(sa.exc.IntegrityError)
async def sa_integrity_error_exception_handler(
    request: Request, exc: sa.exc.IntegrityError
):
    return ORJSONResponse(status_code=409, content={"message": str(exc)})
