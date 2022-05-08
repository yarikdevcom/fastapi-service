import asyncio

import aioredis
import sqlalchemy as sa
from celery import Celery
from sqlalchemy.ext.asyncio import create_async_engine

METADATA = sa.MetaData()


def get_redis(url: str):
    redis = aioredis.from_url(url)
    yield redis


def get_celery():
    celery = Celery(
        "tasks", backend="redis://localhost/2", broker="redis://localhost/2"
    )
    celery.conf.result_backend_transport_options = {
        "retry_policy": {"timeout": 2.0}
    }
    celery.conf.broker_transport_options = {
        "result_chord_ordered": True,
        "visibility_timeout": 60 * 60 * 24,
    }
    celery.conf.update(
        worker_cancel_long_running_tasks_on_connection_loss=True,
        task_serializer="msgpack",
        accept_content=["msgpack"],
        result_serializer="msgpack",
        enable_utc=True,
    )
    yield celery


async def get_db_connection(engine, connections):
    connection = await engine.begin()
    connections.append(connection)
    return connection


async def cleanup_db_connection(connections):
    if not connections:
        return
    conn = connections.popleft()
    while not conn.closed:
        try:
            await conn.close()
        except sa.exc.InterfaceError:
            await asyncio.sleep(0.1)


async def get_db_engine(
    url: str,
    echo: bool,
    pool_size: int,
    max_overflow: int,
    pool_timeout: int,
    connections: list,
):
    engine = create_async_engine(
        url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
    )

    yield engine

    while connections:
        await cleanup_db_connection(connections)

    await engine.dispose()
