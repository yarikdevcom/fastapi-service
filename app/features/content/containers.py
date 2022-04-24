from dependency_injector import containers, providers

from ...resources.services import ModelQueryService
from . import API
from .models import Content
from .tables import CONTENT_TABLE


class ContentContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    api = providers.Object(API)
    resources = providers.DependenciesContainer(
        db=providers.DependenciesContainer()
    )

    content_query = providers.Factory(
        ModelQueryService, resources.db.connection, CONTENT_TABLE, Content
    )
