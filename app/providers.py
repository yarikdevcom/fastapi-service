import aioredis

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine
from aioredlock import Aioredlock

POSTGRES = create_async_engine(
    "postgresql+asyncpg://ps:ps@localhost:5432/ps", echo=True
)
METADATA = sa.MetaData()

REDIS = aioredis.from_url("redis://localhost/1")
REDLOCK = Aioredlock("redis://localhost/1")


async def get_db_connnection():
    """Get database connection with auto-commit."""
    connection = await POSTGRES.begin()

    try:
        yield connection
    except Exception:
        await connection.rollback()
        raise
    finally:
        await connection.close()
