import sqlalchemy as sa

from dependency_injector import containers, providers
from collections import deque

from .resources import (
    get_db_connection,
    get_db_engine,
    cleanup_db_connections,
    get_celery,
    get_redis,
)
from .models import Content
from .tables import CONTENT_TABLE
from .services import ModelCursorService, ModelQueryService


class DBContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    connections = providers.Singleton(deque)
    metadata = providers.Singleton(sa.MetaData)
    engine = providers.Resource(
        get_db_engine,
        url=config.url,
        echo=config.echo,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
        pool_timeout=config.pool_timeout,
        connections=connections,
    )
    cleanup = providers.Coroutine(cleanup_db_connections, connections)
    connection = providers.Coroutine(get_db_connection, engine, connections)


class ModelQueryContainer(containers.DeclarativeContainer):
    db = providers.DependenciesContainer()
    model = providers.Dependency()
    table = providers.Dependency()
    cursor = providers.Factory(ModelCursorService, db.connection, model)
    query = providers.Factory(ModelQueryService, cursor, table)


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration(
        default={
            "db": {
                "url": "postgresql+asyncpg://app:app@localhost:5432/app",
                "echo": False,
                "pool_size": 30,
                "max_overflow": 10,
                "pool_timeout": 10,
            },
            "redis": {"url": "redis://localhost/1"},
        }
    )
    db = providers.Container(DBContainer, config=config.db)
    celery = providers.Resource(get_celery)
    redis = providers.Resource(get_redis, url=config.redis.url)
    content = providers.Container(
        ModelQueryContainer, db=db, model=Content, table=CONTENT_TABLE
    )
