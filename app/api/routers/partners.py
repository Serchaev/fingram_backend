from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.partners import Partners
from app.api.services.partners import PartnersService
from app.core import db_factory

router = APIRouter(
    prefix="/partners",
    tags=["Партнеры"],
)


@router.get("")
async def get_partners(session: AsyncSession = Depends(db_factory.session_depends)) -> list[Partners]:
    return await PartnersService.get_partners(session=session)
