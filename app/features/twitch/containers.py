from dependency_injector import containers, providers

from ...resources.containers import ModelDataContainer

from . import API
from .models import Bot, Channel
from .tables import BOT_TABLE, CHANNEL_TABLE


class TwitchContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    resources = providers.DependenciesContainer(
        db=providers.DependenciesContainer()
    )

    api = providers.Object(API)
    bot = providers.Container(
        ModelDataContainer,
        db=resources.db,
        model=Bot,
        table=BOT_TABLE,
    )
    channel = providers.Container(
        ModelDataContainer,
        db=resources.db,
        model=Channel,
        table=CHANNEL_TABLE
    )
