from dependency_injector import containers, providers

from .resources.containers import ResourcesContainer
from .features import FeaturesContainer


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration(
        default={
            "resources": {
                "db": {
                    "url": "postgresql+asyncpg://app:app@localhost:5432/app",
                    "echo": False,
                    "pool_size": 30,
                    "max_overflow": 10,
                    "pool_timeout": 10,
                },
                "redis": {"url": "redis://localhost/1"},
            }
        }
    )

    resources = providers.Container(
        ResourcesContainer, config=config.resources
    )
    features = providers.Container(
        FeaturesContainer, config=config.features, resources=resources
    )
