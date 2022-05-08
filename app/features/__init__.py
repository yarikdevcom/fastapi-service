from dependency_injector import containers, providers

from .content.containers import ContentContainer


class FeaturesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    resources = providers.DependenciesContainer()
    content: ContentContainer = providers.Container(
        ContentContainer, resources=resources, config=config.content
    )  # type: ignore
