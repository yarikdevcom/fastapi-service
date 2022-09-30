from dependency_injector import containers, providers

from ...resources.containers import ResourcesContainer

# from .services import ContentCRUD
# from .tables import CONTENT_TABLE


class ContentContainer(containers.DynamicContainer):
    config = providers.Configuration()
    resources: ResourcesContainer = providers.DependenciesContainer(
        db=providers.DependenciesContainer()
    )  # type: ignore

    # crud = providers.Factory(ContentCRUD, CONTENT_TABLE, resources.db.engine)
