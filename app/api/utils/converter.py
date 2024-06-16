from functools import wraps
from typing import Awaitable, Callable, List, Sequence, Type, TypeVar, Union

from pydantic import BaseModel

from app.core.models import Base

T = TypeVar("T", bound=BaseModel)


def to_pydantic(db_object: Base, pydantic_model: Type[T]) -> T:
    """
    Преобразует объект модели SQLAlchemy в соответствующую модель Pydantic.

    Аргументы:
        db_object: Объект модели SQLAlchemy, который необходимо преобразовать.
        pydantic_model: Класс модели Pydantic, в который необходимо преобразовать объект SQLAlchemy.

    Возвращает:
        T: Объект модели Pydantic, созданный на основе данных из объекта модели SQLAlchemy.

    Пример:
        class User(Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True, index=True)
            name = Column(String, index=True)
            email = Column(String, unique=True, index=True)

        class UserPydantic(BaseModel):
            id: int
            name: str
            email: str

            class Config:
                orm_mode = True

        user = User(id=1, name="John Doe", email="john.doe@example.com")
        user_pydantic = to_pydantic(user, UserPydantic)
    """
    return pydantic_model(**db_object.__dict__)


def convert_model(
    pydantic_model: Type[T],
) -> Callable[
    [Callable[..., Awaitable[Union[None, Base, List[Base]]]]], Callable[..., Awaitable[Union[None, T, List[T]]]]
]:
    """
    Декоратор для преобразования моделей SQLAlchemy в модели Pydantic.

    Предназначен для использования с асинхронными функциями, которые возвращают
    либо один экземпляр модели SQLAlchemy, либо список экземпляров модели SQLAlchemy. Он преобразует
    модели SQLAlchemy в их соответствующие модели Pydantic.

    Аргументы:
        pydantic_model: Класс модели Pydantic, в который должны быть преобразованы модель(и) SQLAlchemy.

    Примеры:
        @convert_model(UserPydantic)
        async def get_user(user_id: int) -> User:
            # Реализация функции, возвращающей экземпляр SQLAlchemy модели User
            ...

        @convert_model(UserPydantic)
        async def get_users() -> List[User]:
            # Реализация функции, возвращающей список экземпляров SQLAlchemy модели User
            ...
    """

    def decorator(
        func: Callable[..., Awaitable[Union[None, Base, List[Base]]]]
    ) -> Callable[..., Awaitable[Union[None, T, List[T]]]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> list[BaseModel] | BaseModel | None:
            db_objects = await func(*args, **kwargs)
            if db_objects is None:
                return None
            if isinstance(db_objects, Sequence):
                return [pydantic_model(**db_object.__dict__) for db_object in db_objects]
            return pydantic_model(**db_objects.__dict__)

        return wrapper

    return decorator
