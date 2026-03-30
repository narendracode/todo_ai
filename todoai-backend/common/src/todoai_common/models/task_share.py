import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class TaskShare(Base, TimestampMixin):
    __tablename__ = "task_shares"
    __table_args__ = (UniqueConstraint("task_id", "user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    can_edit: Mapped[bool] = mapped_column(default=False, nullable=False)

    task: Mapped["Task"] = relationship("Task", back_populates="shares")  # noqa: F821
    user: Mapped["User"] = relationship("User", back_populates="shared_tasks")  # noqa: F821
