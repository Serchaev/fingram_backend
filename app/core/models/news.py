from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base
from app.core.models.utils import TimeStampModelMixin


class News(Base, TimeStampModelMixin):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    body: Mapped[str]
    date = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
