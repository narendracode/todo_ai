import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(
        String(320), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(1024))
    google_sub: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    owned_tasks: Mapped[list["Task"]] = relationship(  # noqa: F821
        "Task", foreign_keys="Task.owner_id", back_populates="owner"
    )
    assigned_tasks: Mapped[list["Task"]] = relationship(  # noqa: F821
        "Task", foreign_keys="Task.assigned_to_id", back_populates="assignee"
    )
    shared_tasks: Mapped[list["TaskShare"]] = relationship(  # noqa: F821
        "TaskShare", back_populates="user"
    )
