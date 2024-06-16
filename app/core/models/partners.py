from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base
from app.core.models.utils import TimeStampModelMixin


class Partners(Base, TimeStampModelMixin):
    __tablename__ = "partners"

    id: Mapped[int] = mapped_column(primary_key=True)
    path_logo: Mapped[str]
    place: Mapped[int]
