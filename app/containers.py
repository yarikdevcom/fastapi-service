from dependency_injector import containers, providers

from .providers import get_db_connnection
from .models import Content
from .tables import CONTENT_TABLE
from .services import ModelDBService, ModelTableService


class ContentContainer(containers.DeclarativeContainer):
    connection = providers.Resource(get_db_connnection)
    db = providers.Factory(ModelDBService, connection, Content)
    query = providers.Factory(ModelTableService, db, CONTENT_TABLE)
