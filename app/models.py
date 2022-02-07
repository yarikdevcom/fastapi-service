import typing as T

from pydantic import BaseModel


class ContentIn(BaseModel):
    url: str


class Content(ContentIn):
    id: int
    url: str
    body: T.Optional[str]
