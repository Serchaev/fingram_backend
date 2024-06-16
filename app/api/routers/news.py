from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.news import News, NewsInput, NewsPaginator
from app.api.schemas.paginator import Paginator
from app.api.services.news import NewsService
from app.core import db_factory

router = APIRouter(
    prefix="/news",
    tags=["Новости"],
)


@router.get("")
async def get_news(
    paginator: Paginator = Depends(Paginator),
    session: AsyncSession = Depends(db_factory.session_depends),
) -> NewsPaginator:
    return await NewsService.get_news(session=session, paginator=paginator)


@router.post("")
async def add_new(
    new: NewsInput,
    session: AsyncSession = Depends(db_factory.session_depends),
):
    return await NewsService.add_new(session=session, new=new)


@router.get("/{news_id}")
async def get_new(
    news_id: int,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> News:
    new = await NewsService.get_new(session=session, news_id=news_id)
    if new is None:
        raise HTTPException(status_code=404, detail=f"Мероприятие {news_id} не найдено")
    return new


@router.put("/{news_id}")
async def update_new(
    news_id: int,
    new: NewsInput,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> News:
    new = await NewsService.update_new(session=session, news_id=news_id, new=new)
    if new is None:
        raise HTTPException(status_code=404, detail=f"Мероприятие {news_id} не найдено")
    return new


@router.delete("/{news_id}")
async def delete_new(
    news_id: int,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> None:
    await NewsService.delete_new(session=session, news_id=news_id)
