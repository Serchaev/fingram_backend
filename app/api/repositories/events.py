from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.events import Events as EventsSchema
from app.api.schemas.events import EventsInput
from app.api.schemas.paginator import Paginator
from app.api.utils.converter import convert_model
from app.core.models import Events


class EventsRepo:

    @classmethod
    @convert_model(EventsSchema)
    async def get_events(cls, session: AsyncSession, paginator: Paginator = None) -> list[Events]:
        stmt = select(Events)
        if paginator:
            stmt = stmt.offset((paginator.page - 1) * paginator.size)
            stmt = stmt.limit(paginator.size)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def count(cls, session: AsyncSession):
        stmt = select(func.count()).select_from(Events)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_event(cls, session: AsyncSession, event_id: int) -> Events:
        stmt = select(Events).where(Events.id == event_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def add_event(cls, session: AsyncSession, event: EventsInput) -> Events:
        stmt = insert(Events).values(
            title=event.title,
            body=event.body,
            organizer=event.organizer,
            address=event.address,
            count_seats=event.count_seats,
            time_start=event.time_start,
            time_end=event.time_end,
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def update_event(cls, session: AsyncSession, event: EventsInput, event_id: int) -> Events:
        stmt = (
            update(Events)
            .values(
                title=event.title,
                body=event.body,
                organizer=event.organizer,
                address=event.address,
                count_seats=event.count_seats,
                time_start=event.time_start,
                time_end=event.time_end,
            )
            .where(Events.id == event_id)
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def delete_event(cls, session: AsyncSession, event_id: int) -> Events:
        stmt = delete(Events).where(Events.id == event_id)
        await session.execute(stmt)
        await session.commit()
