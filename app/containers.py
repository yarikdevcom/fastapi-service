from dependency_injector import containers, providers

from .providers import get_db_connnection
from .models import Channel
from .tables import CHANNEL_TABLE
from .services import ModelDBService, ModelTableService


class ChannelContainer(containers.DeclarativeContainer):
    connection = providers.Resource(get_db_connnection)
    db = providers.Factory(ModelDBService, connection, Channel)
    query = providers.Factory(ModelTableService, db, CHANNEL_TABLE)
