from dependency_injector import containers, providers

from .features import FeaturesContainer
from .resources.containers import ResourcesContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=(".features.content",)
    )
    config = providers.Configuration()
    resources = providers.Container(
        ResourcesContainer, config=config.resources
    )
    features = providers.Container(
        FeaturesContainer, config=config.features, resources=resources
    )
