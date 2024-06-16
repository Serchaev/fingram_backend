from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, func


class TimeStampModelMixin:
    __abstract__ = True

    date_created = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="Дата создания",
        comment="Дата создания",
    )
    date_updated = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),  # TODO: перенос на триггер
        doc="Дата редактирования",
        comment="Дата редактирования",
    )
