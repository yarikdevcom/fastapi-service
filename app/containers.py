from dependency_injector import containers, providers

from .resources import DBContainer, get_celery, get_redis
from .content.containers import ContentContainer


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

    content = providers.Container(ContentContainer, db=db)
