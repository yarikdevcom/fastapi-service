import asyncio

import aioredis

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine
from celery import Celery

POSTGRES = create_async_engine(
    "postgresql+asyncpg://ps:ps@localhost:5432/ps", future=True, echo=True
)
METADATA = sa.MetaData()

REDIS = aioredis.from_url("redis://localhost/1")

CELERY = Celery(
    "tasks", backend="redis://localhost/2", broker="redis://localhost/2"
)
CELERY.conf.result_backend_transport_options = {
    "retry_policy": {"timeout": 120.0}
}
CELERY.conf.broker_transport_options = {
    "result_chord_ordered": True,
    "visibility_timeout": 60 * 60 * 24,
}
CELERY.conf.update(
    task_serializer="msgpack",
    accept_content=["msgpack"],
    result_serializer="msgpack",
    enable_utc=True,
)
CELERY.loop = asyncio.new_event_loop()


async def get_db_connnection():
    """Get database connection with auto-commit."""
    async with POSTGRES.connect() as connection:
        try:
            await connection.begin()
            yield connection
            await connection.commit()
        except:  # noqa
            await connection.rollback()
            raise
