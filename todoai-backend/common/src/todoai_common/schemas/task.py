import uuid
from datetime import date, datetime

from pydantic import BaseModel

from ..enums import Priority, TaskStatus, Visibility


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    visibility: Visibility = Visibility.PRIVATE
    time_from: datetime | None = None
    time_to: datetime | None = None
    expiry_date: date | None = None
    is_recurring: bool = False
    recurrence_rule: str | None = None
    assigned_to_id: uuid.UUID | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: Priority | None = None
    status: TaskStatus | None = None
    visibility: Visibility | None = None
    time_from: datetime | None = None
    time_to: datetime | None = None
    expiry_date: date | None = None
    is_recurring: bool | None = None
    recurrence_rule: str | None = None
    assigned_to_id: uuid.UUID | None = None


class TaskShareCreate(BaseModel):
    user_id: uuid.UUID
    can_edit: bool = False


class TaskShareOut(BaseModel):
    id: uuid.UUID
    task_id: uuid.UUID
    user_id: uuid.UUID
    can_edit: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskOut(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    assigned_to_id: uuid.UUID | None
    title: str
    description: str | None
    priority: Priority
    status: TaskStatus
    visibility: Visibility
    time_from: datetime | None
    time_to: datetime | None
    expiry_date: date | None
    is_recurring: bool
    recurrence_rule: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedTasks(BaseModel):
    items: list[TaskOut]
    total: int
    page: int
    size: int
    pages: int
