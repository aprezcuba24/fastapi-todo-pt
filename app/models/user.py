from .base import Base
from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    items: Mapped[List["Item"]] = relationship(back_populates="owner")

    __table_args__ = (Index("ix_users_id", "id"),)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"
