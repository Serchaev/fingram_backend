from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.events import Events, EventsInput, EventsPaginator
from app.api.schemas.paginator import Paginator
from app.api.services.events import EventsService
from app.core import db_factory

router = APIRouter(
    prefix="/events",
    tags=["Мероприятия"],
)


@router.get("")
async def get_events(
    paginator: Paginator = Depends(Paginator),
    session: AsyncSession = Depends(db_factory.session_depends),
) -> EventsPaginator:
    return await EventsService.get_events(session=session, paginator=paginator)


@router.post("")
async def add_event(
    event: EventsInput,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> EventsPaginator:
    return await EventsService.add_event(session=session, event=event)


@router.get("/{event_id}")
async def get_event(
    event_id: int,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> Events:
    event = await EventsService.get_event(session=session, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"Мероприятие {event_id} не найдено")
    return event


@router.put("/{event_id}")
async def update_event(
    event_id: int,
    event: EventsInput,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> Events:
    event = await EventsService.update_event(session=session, event_id=event_id, event=event)
    if event is None:
        raise HTTPException(status_code=404, detail=f"Мероприятие {event_id} не найдено")
    return event


@router.delete("/{event_id}")
async def delete_event(
    event_id: int,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> None:
    await EventsService.delete_event(session=session, event_id=event_id)
