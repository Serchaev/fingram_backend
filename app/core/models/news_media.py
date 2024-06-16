from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base
from app.core.models.utils import TimeStampModelMixin


class NewsMedia(Base, TimeStampModelMixin):
    __tablename__ = "news_media"

    id: Mapped[int] = mapped_column(primary_key=True)
    news_id: Mapped[int] = mapped_column(ForeignKey(column="news.id", ondelete="cascade"))
    path_file: Mapped[str]
