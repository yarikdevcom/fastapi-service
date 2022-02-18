from dependency_injector import containers, providers

from .. import resources

from .models import Content
from .tables import CONTENT_TABLE


class ContentContainer(containers.DeclarativeContainer):
    db = providers.DependenciesContainer()

    data = providers.Container(
        resources.ModelDataContainer,
        db=db,
        model=Content,
        table=CONTENT_TABLE,
    )
