import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..enums import Priority, TaskStatus, Visibility
from .base import Base, TimestampMixin


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assigned_to_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[Priority] = mapped_column(
        SAEnum(Priority), nullable=False, default=Priority.MEDIUM
    )
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus), nullable=False, default=TaskStatus.TODO
    )
    visibility: Mapped[Visibility] = mapped_column(
        SAEnum(Visibility), nullable=False, default=Visibility.PRIVATE
    )

    time_from: Mapped[datetime | None]
    time_to: Mapped[datetime | None]
    expiry_date: Mapped[date | None]

    is_recurring: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    recurrence_rule: Mapped[str | None] = mapped_column(String(1024))

    owner: Mapped["User"] = relationship(  # noqa: F821
        "User", foreign_keys=[owner_id], back_populates="owned_tasks"
    )
    assignee: Mapped["User | None"] = relationship(  # noqa: F821
        "User", foreign_keys=[assigned_to_id], back_populates="assigned_tasks"
    )
    shares: Mapped[list["TaskShare"]] = relationship(  # noqa: F821
        "TaskShare", back_populates="task", cascade="all, delete-orphan"
    )
