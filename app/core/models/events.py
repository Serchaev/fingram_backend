from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base
from app.core.models.utils import TimeStampModelMixin


class Events(Base, TimeStampModelMixin):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    body: Mapped[str]
    organizer: Mapped[str]
    address: Mapped[str]
    count_seats: Mapped[int]
    time_start = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    time_end = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
