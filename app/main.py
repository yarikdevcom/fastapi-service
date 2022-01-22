from fastapi import FastAPI

from . import api
from .containers import ChannelContainer


def create_app():
    app = FastAPI()

    # containers
    channel_container = ChannelContainer()
    channel_container.wire(modules=(api,))

    app.channel_container = channel_container

    # routes
    app.include_router(api.router)

    return app


app = create_app()
