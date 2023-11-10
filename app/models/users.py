from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.configuration.database.base import Base


class User(Base):
    name: Mapped[str] = mapped_column(String(32), unique=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self) -> str:
        return str(self)
