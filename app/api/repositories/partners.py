from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Partners


class PartnersRepo:

    @classmethod
    async def get_partners(cls, session: AsyncSession) -> list[Partners]:
        stmt = select(Partners)
        result = await session.execute(stmt)
        return result.scalars().all()
