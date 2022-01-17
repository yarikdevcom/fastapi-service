import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

URL = "postgresql+asyncpg://ps:ps@localhost:5432/ps"
ENGINE = create_async_engine(URL, echo=True)
METADATA = sa.MetaData()

HELLO_WORLD_TABLE = sa.Table(
    "hello_world",
    METADATA,
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("message", sa.VARCHAR(255), nullable=False),
)
