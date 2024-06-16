import datetime

from pydantic import BaseModel

from app.api.schemas.paginator import PaginatorData


class NewsInput(BaseModel):
    title: str
    body: str
    date: datetime.datetime


class News(NewsInput):
    id: int


class NewsPaginator(PaginatorData):
    items: list[News]
