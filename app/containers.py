import os

from dependency_injector import containers, providers

# from .features import FeaturesContainer
from .resources.containers import ResourcesContainer

# TODO: implement timeout for waiting service connection up to 1 min
# so we can skip part with docker service management


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=(".features.content",)
    )
    config = providers.Configuration(
        yaml_files=[os.environ.get("APP_CONFIG_PATH", "./config.yaml")]
    )
    resources: ResourcesContainer = providers.Container(
        ResourcesContainer, config=config.resources
    )  # type: ignore
    # features: FeaturesContainer = providers.Container(
    # FeaturesContainer, config=config.features, resources=resources
    # )  # type: ignore
