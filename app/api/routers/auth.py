from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends.auth_depends import get_current_auth_user
from app.api.schemas.auth import (
    LoginSchemaAnswer,
    LoginSchemaBody,
    RefreshSchema,
    RegisterSchemaAnswer,
    RegisterSchemaBody,
)
from app.api.services.auth import AuthService
from app.core import db_factory

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    register_body: RegisterSchemaBody,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> RegisterSchemaAnswer:
    return await AuthService.register(
        session=session,
        new_user=register_body.model_dump(),
    )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginSchemaBody,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> LoginSchemaAnswer:
    tokens = await AuthService.login(session=session, login_data=login_data)
    return {
        "refresh_token": tokens["refresh_token"],
        "access_token": tokens["access_token"],
        "token_type": "Bearer",
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    payload=Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_factory.session_depends),
):
    await AuthService.logout(session=session, payload=payload)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    token: RefreshSchema,
    session: AsyncSession = Depends(db_factory.session_depends),
):
    tokens = await AuthService.refresh(session=session, refresh_token=token.refresh_token)
    return {
        "refresh_token": tokens["refresh_token"],
        "access_token": tokens["access_token"],
        "token_type": "Bearer",
    }
