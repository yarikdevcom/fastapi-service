import typing as T

from datetime import datetime

from pydantic import BaseModel


class ChannelIn(BaseModel):
    url: str


class Channel(ChannelIn):
    id: int
    url: str
    start_listen_at: T.Optional[datetime]
    ping_listen_at: T.Optional[datetime]
    stop_listen_at: T.Optional[datetime]
    ignore: bool = False
    active: bool = False
