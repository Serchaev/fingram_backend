from pydantic import BaseModel


class Paginator(BaseModel):
    page: int = 1
    size: int = 10


class PaginatorData(Paginator):
    pages: int
    total: int
