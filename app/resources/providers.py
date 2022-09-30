from contextlib import asynccontextmanager

import aioredis
import asyncpg
import sqlalchemy as sa
from celery import Celery
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

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


async def get_db_pool(
    url: str,
    min_size: int,
    max_size: int,
):
    url = url.replace("+asyncpg", "")
    pool = await asyncpg.create_pool(url, min_size=min_size, max_size=max_size)
    yield pool
    await pool.close()


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
        # pool_size=pool_size,
        # max_overflow=max_overflow,
        # pool_timeout=pool_timeout,
        poolclass=NullPool,
        connect_args={"server_settings": {"jit": "off"}},
    )
    yield engine
    await engine.dispose()


class ConnectionProvider:
    def __init__(self, pool: asyncpg.Pool):
        self.raw = None
        self.pool = pool

    def prepare(self, query):
        compiled = query.compile()
        query = str(compiled)
        for index, key in enumerate(compiled.params, 1):
            query = query.replace(f":{key}", f"${index}")
        # print('query', query)
        return query, compiled.params.values()

    # def use(self, connection=None):
    #     if self.raw:
    #         pass
    #     old_connection = self.raw
    #     self.raw = connection.raw
    #     yield
    #     self.raw = old_connection

    @asynccontextmanager
    async def acquire(self):
        if not self.raw:
            async with self.pool.acquire() as raw:
                yield raw
        else:
            yield self.raw

    async def scalar(self, query, commit: bool = False):
        return (await self.prepare(query, commit)).scalar()

    async def one(self, query, commit: bool = False) -> dict | None:
        query, params = self.prepare(query)
        async with self.acquire() as raw:
            row = await raw.fetchrow(query, *params)
        return dict(row) if row else None

    async def many(self, query, commit: bool = False) -> list[dict]:
        query, params = self.prepare(query)
        async with self.acquire() as raw:
            return [dict(row) for row in (await raw.fetch(query, *params))]
