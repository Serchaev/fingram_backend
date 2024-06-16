import datetime
import re

from pydantic import BaseModel, EmailStr, constr, field_validator


class RegisterSchema(BaseModel):
    username: constr(min_length=3, max_length=20)
    password: constr(min_length=8, max_length=20)
    email: EmailStr
    first_name: str
    second_name: str
    patronymic: str
    phone_number: str
    birthday: datetime.datetime

    @field_validator("username")
    def validate_username(cls, v: str):
        pattern = r"^[a-zA-Z0-9_]+$"  # Разрешает буквы, цифры и нижнее подчеркивание
        if not re.match(pattern, v):
            raise ValueError("Username can contain only letters, numbers and underscores.")
        return v

    @field_validator("phone_number")
    def validate_phone_number(cls, v: str):
        if not v.startswith("+7"):
            raise ValueError('Номер телефона должен начинаться с "+7".')
        if len(v) != 12:
            raise ValueError("Номер телефона должен состоять из 11 цифр.")
        return v


class RegisterSchemaBody(RegisterSchema):
    pass


class RegisterSchemaAnswer(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    second_name: str
    patronymic: str
    phone_number: str
    birthday: datetime.datetime


class LoginSchemaBody(BaseModel):
    login: str
    password: str


class LoginSchemaAnswer(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str


class RefreshSchema(BaseModel):
    refresh_token: str
