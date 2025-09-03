from .base import Base
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum


class StatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(30))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="items")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum, name="status_enum"), nullable=False, default=StatusEnum.pending
    )

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, title={self.title!r}, status={self.status!r})"
