from fastapi import FastAPI

from . import api, tasks
from .containers import ContentContainer


__version__ = "0.1.0"


APP = FastAPI()

# containers
APP.channel_container = ContentContainer()
APP.channel_container.wire(modules=(api, tasks))

# routes
APP.include_router(api.router)
