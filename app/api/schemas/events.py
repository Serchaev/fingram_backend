import datetime

from pydantic import BaseModel

from app.api.schemas.paginator import PaginatorData


class EventsInput(BaseModel):
    title: str
    body: str
    organizer: str
    address: str
    count_seats: int
    time_start: datetime.datetime
    time_end: datetime.datetime


class Events(EventsInput):
    id: int


class EventsPaginator(PaginatorData):
    items: list[Events]
