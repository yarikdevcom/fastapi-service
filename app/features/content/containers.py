from dependency_injector import containers, providers

from ...resources.containers import ModelDataContainer

from . import API
from .models import Content
from .tables import CONTENT_TABLE


class ContentContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    resources = providers.DependenciesContainer(
        db=providers.DependenciesContainer()
    )

    api = providers.Object(API)
    data = providers.Container(
        ModelDataContainer,
        db=resources.db,
        model=Content,
        table=CONTENT_TABLE,
    )
