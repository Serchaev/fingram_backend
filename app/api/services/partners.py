from sqlalchemy.ext.asyncio import AsyncSession

from app.api.repositories.partners import PartnersRepo
from app.core.models import Partners


class PartnersService:

    @classmethod
    async def get_partners(cls, session: AsyncSession) -> list[Partners]:
        return await PartnersRepo.get_partners(session=session)
