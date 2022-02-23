from dependency_injector import containers, providers

from .resources.containers import ResourcesContainer
from .features import FeaturesContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=(".features.content", ".features.twitch")
    )
    config = providers.Configuration()
    resources = providers.Container(
        ResourcesContainer, config=config.resources
    )
    features = providers.Container(
        FeaturesContainer, config=config.features, resources=resources
    )
