from dependency_injector import containers, providers

from ...resources.containers import ModelDataContainer

from . import API
from .models import Bot
from .tables import BOT_TABLE


class BotContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    resources = providers.DependenciesContainer(
        db=providers.DependenciesContainer()
    )

    api = providers.Object(API)
    data = providers.Container(
        ModelDataContainer,
        db=resources.db,
        model=Bot,
        table=BOT_TABLE,
    )
