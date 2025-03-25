from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List
from .base import Base

if TYPE_CHECKING:
    from .spending import Spending


class User(Base):
    chat_id: Mapped[str] = mapped_column(unique=True)
    spendings: Mapped[List["Spending"]] = relationship(
        back_populates="user",
        uselist=True,
    )
