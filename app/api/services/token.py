from fastapi import HTTPException, status
from jwt import InvalidTokenError

from app.auth.utils import decode_jwt, encode_jwt
from app.core.models import User


class TokenService:

    @classmethod
    async def generate_tokens(cls, user: User) -> dict[str, str]:
        payload = {
            "sub": user.id,
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "second_name": user.second_name,
            "patronymic": user.patronymic,
            "phone_number": user.phone_number,
            "birthday": user.birthday.strftime("%Y-%m-%d %H:%M:%SS"),
        }
        access_token = encode_jwt(payload=payload, expire_minutes=10)
        refresh_token = encode_jwt(payload=payload, expire_minutes=60)

        return {"access_token": access_token, "refresh_token": refresh_token}

    @classmethod
    async def validate_token(cls, token: str):
        try:
            return decode_jwt(token=token)
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token error",
            )
