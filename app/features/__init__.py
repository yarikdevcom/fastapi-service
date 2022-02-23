from dependency_injector import containers, providers

from .content.containers import ContentContainer
from .twitch.containers import BotContainer


class FeaturesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    resources = providers.DependenciesContainer()
    content = providers.Container(
        ContentContainer, resources=resources, config=config.content
    )
    bot = providers.Container(
        BotContainer, resources=resources, config=config.bot
    )
