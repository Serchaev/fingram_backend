from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User


class UserRepo:
    @classmethod
    async def find_one(cls, session: AsyncSession, username: str | None = None, email: str | None = None) -> User:
        stmt = select(User)
        if username is not None:
            stmt = stmt.where(User.username == username)
        if email is not None:
            stmt = stmt.where(User.email == email)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def add_user(cls, session: AsyncSession, new_user: dict):
        stmt = (
            insert(User)
            .values(
                username=new_user.get("username"),
                hashed_password=new_user.get("hashed_password"),
                email=new_user.get("email"),
                first_name=new_user.get("first_name"),
                second_name=new_user.get("second_name"),
                patronymic=new_user.get("patronymic"),
                phone_number=new_user.get("phone_number"),
                birthday=new_user.get("birthday"),
            )
            .returning(User)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalars().one()
