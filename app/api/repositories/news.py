from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.news import News as NewsSchema
from app.api.schemas.news import NewsInput
from app.api.schemas.paginator import Paginator
from app.api.utils.converter import convert_model
from app.core.models import News


class NewsRepo:

    @classmethod
    @convert_model(NewsSchema)
    async def get_news(cls, session: AsyncSession, paginator: Paginator = None) -> list[News]:
        stmt = select(News)
        if paginator:
            stmt = stmt.offset((paginator.page - 1) * paginator.size)
            stmt = stmt.limit(paginator.size)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def count(cls, session: AsyncSession):
        stmt = select(func.count()).select_from(News)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_new(cls, session: AsyncSession, news_id: int) -> News:
        stmt = select(News).where(News.id == news_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def add_new(cls, session: AsyncSession, new: NewsInput) -> News:
        stmt = insert(News).values(
            title=new.title,
            body=new.body,
            date=new.date,
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def update_new(cls, session: AsyncSession, new: NewsInput, news_id: int) -> News:
        stmt = (
            update(News)
            .values(
                title=new.title,
                body=new.body,
                date=new.date,
            )
            .where(News.id == news_id)
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def delete_new(cls, session: AsyncSession, news_id: int) -> News:
        stmt = delete(News).where(News.id == news_id)
        await session.execute(stmt)
        await session.commit()
