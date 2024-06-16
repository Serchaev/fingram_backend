from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base
from app.core.models.utils import TimeStampModelMixin


class User(Base, TimeStampModelMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[bytes]
    email: Mapped[str]
    first_name: Mapped[str]
    second_name: Mapped[str]
    patronymic: Mapped[str]
    phone_number: Mapped[str]
    birthday = mapped_column(DateTime(timezone=True), nullable=False)
