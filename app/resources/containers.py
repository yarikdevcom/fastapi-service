from dependency_injector import containers, providers

from .providers import ConnectionProvider, get_celery, get_db_engine, get_redis


class DBContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    engine = providers.Resource(
        get_db_engine,
        url=config.url,
        echo=config.echo,
        pool_size=config.pool_size.as_int(),
        max_overflow=config.max_overflow.as_int(),
        pool_timeout=config.pool_timeout.as_int(),
    )
    connection = providers.Factory(ConnectionProvider, engine)


class ResourcesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db: DBContainer = providers.Container(
        DBContainer, config=config.db
    )  # type: ignore
    celery = providers.Resource(get_celery)
    redis = providers.Resource(get_redis, url=config.redis.url)
