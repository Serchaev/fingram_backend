from math import ceil

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.repositories.news import NewsRepo
from app.api.schemas.news import NewsInput, NewsPaginator
from app.api.schemas.paginator import Paginator
from app.core.models import News


class NewsService:

    @classmethod
    async def get_news(cls, session: AsyncSession, paginator: Paginator = None) -> list[News]:
        result = await NewsRepo.get_news(session=session, paginator=paginator)
        count = await NewsRepo.count(session=session)
        return NewsPaginator(
            items=result,
            page=paginator.page,
            size=paginator.size,
            pages=ceil(count / paginator.size),
            total=len(result),
        )

    @classmethod
    async def get_new(cls, session: AsyncSession, news_id: int) -> News:
        try:
            return await NewsRepo.get_new(session=session, news_id=news_id)
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def add_new(cls, session: AsyncSession, new: NewsInput) -> News:
        return await NewsRepo.add_new(session=session, new=new)

    @classmethod
    async def update_new(cls, session: AsyncSession, news_id: int, new: NewsInput) -> News:
        await NewsRepo.update_new(session=session, news_id=news_id, new=new)
        return await cls.get_new(session=session, news_id=news_id)

    @classmethod
    async def delete_new(cls, session: AsyncSession, news_id: int) -> News:
        await NewsRepo.delete_new(session=session, news_id=news_id)
