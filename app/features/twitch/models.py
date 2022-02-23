import typing as T

from datetime import datetime
from pydantic import BaseModel


class Bot(BaseModel):
    id: int
    secret_id: str
    client_id: str
    nickname: str
    load: int = 0
    max_load: int = 40


class BotIn(BaseModel):
    secret_id: str
    client_id: str
    nickname: str


class User(BaseModel):
    id: int
    nicknames: list[str]
    ext_id: int


class Message(BaseModel):
    id: int
    content: str
    user_id: int
    channel_id: int


class ChannelIn(BaseModel):
    url: str


class Channel(ChannelIn):
    id: int
    url: str
    start_listen_at: T.Optional[datetime]
    ping_listen_at: T.Optional[datetime]
    stop_listen_at: T.Optional[datetime]
    listen_bot_id: T.Optional[int]
    ignore: bool = False
    active: bool = False


class ChannelAcquire(BaseModel):
    size: int


class BotWithChannels(BaseModel):
    bot: Bot
    channels: list[Channel]
