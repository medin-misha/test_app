from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .user import User


class Spending(Base):
    name: Mapped[str]
    money: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(Date, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="spendings", lazy="selectin")
