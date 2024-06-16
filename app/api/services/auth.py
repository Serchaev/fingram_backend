from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.repositories.token import TokenRepo
from app.api.repositories.user import UserRepo
from app.api.schemas.auth import LoginSchemaBody
from app.api.services.token import TokenService
from app.auth.utils import hash_password, validate_password


class AuthService:
    @classmethod
    async def register(cls, session: AsyncSession, new_user: dict):
        check_username = await UserRepo.find_one(
            session=session,
            username=new_user.get("username"),
        )
        if check_username is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username - {new_user.get('username')} already exists!",
            )
        check_email = await UserRepo.find_one(
            session=session,
            email=new_user.get("email"),
        )
        if check_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email - {new_user.get('email')} already exists!",
            )
        new_user["hashed_password"] = hash_password(new_user["password"])
        new_user.pop("password")
        return await UserRepo.add_user(
            session=session,
            new_user=new_user,
        )

    @classmethod
    async def login(cls, session: AsyncSession, login_data: LoginSchemaBody):
        data = {"username": str(login_data.login)}
        if "@" in login_data.login:
            data["email"] = data.pop("username")
        find_user = await UserRepo.find_one(
            session=session,
            **data,
        )
        if find_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username or password.",
            )
        if not validate_password(login_data.password, find_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username or password.",
            )
        tokens = await TokenService.generate_tokens(find_user)
        token = await TokenRepo.find(session=session, user_id=find_user.id)
        if token is not None:
            token.refresh_token = tokens["refresh_token"]
            await TokenRepo.update(session=session, token=token)
        else:
            await TokenRepo.create(session=session, refresh_token=tokens["refresh_token"], user_id=find_user.id)
        return tokens

    @classmethod
    async def logout(cls, session: AsyncSession, payload: dict):
        await TokenRepo.delete(session=session, payload=payload)

    @classmethod
    async def refresh(cls, session: AsyncSession, refresh_token: str):
        payload = await TokenService.validate_token(token=refresh_token)
        await cls.logout(session=session, payload=payload)
        find_user = await UserRepo.find_one(
            session=session,
            username=payload["username"],
        )
        tokens = await TokenService.generate_tokens(find_user)
        token = await TokenRepo.find(session=session, user_id=find_user.id)
        if token is not None:
            token.refresh_token = tokens["refresh_token"]
            await TokenRepo.update(session=session, token=token)
        else:
            await TokenRepo.create(session=session, refresh_token=tokens["refresh_token"], user_id=find_user.id)
        return tokens
