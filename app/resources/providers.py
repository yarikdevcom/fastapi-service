import typing as TP
from contextlib import asynccontextmanager

import aioredis
import sqlalchemy as sa
from celery import Celery
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

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


async def get_db_engine(
    url: str,
    echo: bool,
    pool_size: int,
    max_overflow: int,
    pool_timeout: int,
):
    engine = create_async_engine(
        f"{url}?prepared_statement_cache_size=100",
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        connect_args={"server_settings": {"jit": "off"}},
    )
    yield engine
    await engine.dispose()


class ConnectionProvider:
    """
    async def somelogic(cn, dal1, dal2):
        await dal1.blah()

        async with cn.transaction(), dal1.inject(cn), dal2.inject(cn):
            await dal1.some_logic()
            await dal2.some_logci()
    """

    def __init__(self, engine):
        self.engine = engine
        self.current: AsyncConnection | None = None

    @asynccontextmanager
    async def inject(
        self, connection: "ConnectionProvider"
    ) -> TP.AsyncGenerator["ConnectionProvider", None]:
        if self.current:
            raise ValueError(
                "Connection already used, you cannot override current one"
            )

        self.current = connection.current
        yield self
        self.current = None

    @asynccontextmanager
    async def acquire(self) -> TP.AsyncGenerator[AsyncConnection, None]:
        if self.current:
            yield self.current
        else:
            async with self.engine.begin() as cn:
                self.current = cn
                yield cn
                self.current = None

    async def execute(self, query) -> None:
        async with self.acquire() as cn:
            await cn.execute(query)

    async def scalar(self, query) -> TP.Any | None:
        async with self.acquire() as cn:
            result = (await cn.execute(query)).scalar()
        return result

    async def one(self, query) -> dict[str, TP.Any]:
        async with self.acquire() as cn:
            row = (await cn.execute(query)).fetchone()
        return dict(row) if row else dict()

    async def many(self, query) -> list[dict[str, TP.Any]]:
        async with self.acquire() as cn:
            rows = (await cn.execute(query)).fetchall()
        return [dict(row) for row in rows]
