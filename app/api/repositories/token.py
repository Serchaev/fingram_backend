from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Token


class TokenRepo:

    @classmethod
    async def find(cls, session: AsyncSession, user_id: int):
        stmt = select(Token).where(Token.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, token: Token):
        stmt = update(Token).values(refresh_token=token.refresh_token).where(Token.id == token.id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def create(cls, session: AsyncSession, refresh_token: str, user_id: int):
        stmt = insert(Token).values(
            user_id=user_id,
            refresh_token=refresh_token,
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def delete(cls, session: AsyncSession, payload: dict):
        stmt = delete(Token).where(Token.user_id == payload["id"])
        await session.execute(stmt)
        await session.commit()
