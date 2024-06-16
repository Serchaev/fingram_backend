from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.repositories.events import EventsRepo
from app.api.schemas.events import EventsInput
from app.api.schemas.news import NewsPaginator
from app.api.schemas.paginator import Paginator
from app.core.models import Events


class EventsService:

    @classmethod
    async def get_events(cls, session: AsyncSession, paginator: Paginator = None) -> list[Events]:
        result = await EventsRepo.get_events(session=session, paginator=paginator)
        count = await EventsRepo.count(session=session)
        return NewsPaginator(
            items=result,
            page=paginator.page,
            size=paginator.size,
            pages=ceil(count / paginator.size),
            total=len(result),
        )

    @classmethod
    async def get_event(cls, session: AsyncSession, event_id: int) -> Events:
        return await EventsRepo.get_event(session=session, event_id=event_id)

    @classmethod
    async def add_event(cls, session: AsyncSession, event: EventsInput) -> Events:
        return await EventsRepo.add_event(session=session, event=event)

    @classmethod
    async def update_event(cls, session: AsyncSession, event_id: int, event: EventsInput) -> Events:
        await EventsRepo.update_event(session=session, event_id=event_id, event=event)
        return await cls.get_event(session=session, event_id=event_id)

    @classmethod
    async def delete_event(cls, session: AsyncSession, event_id: int) -> Events:
        await EventsRepo.delete_event(session=session, event_id=event_id)
