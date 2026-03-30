import math
import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from todoai_common.enums import TaskStatus, Visibility
from todoai_common.models import Task, TaskShare, User
from todoai_common.schemas.task import PaginatedTasks, TaskCreate, TaskOut, TaskUpdate


def _visible_tasks_query(db: Session, user: User):
    return db.query(Task).filter(
        or_(
            Task.owner_id == user.id,
            Task.assigned_to_id == user.id,
            Task.visibility == Visibility.PUBLIC,
            Task.id.in_(
                db.query(TaskShare.task_id).filter(TaskShare.user_id == user.id)
            ),
        )
    )


def list_tasks(
    db: Session,
    user: User,
    status: TaskStatus | None = None,
    priority=None,
    assigned_to: uuid.UUID | None = None,
    page: int = 1,
    size: int = 20,
) -> PaginatedTasks:
    q = _visible_tasks_query(db, user)
    if status:
        q = q.filter(Task.status == status)
    if priority:
        q = q.filter(Task.priority == priority)
    if assigned_to:
        q = q.filter(Task.assigned_to_id == assigned_to)

    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    return PaginatedTasks(
        items=[TaskOut.model_validate(t) for t in items],
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if size else 1,
    )


def get_task(db: Session, user: User, task_id: uuid.UUID) -> Task | None:
    return _visible_tasks_query(db, user).filter(Task.id == task_id).first()


def create_task(db: Session, user: User, data: TaskCreate) -> Task:
    task = Task(
        id=uuid.uuid4(),
        owner_id=user.id,
        **data.model_dump(),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()


def add_share(db: Session, task: Task, user_id: uuid.UUID, can_edit: bool) -> TaskShare:
    share = TaskShare(
        id=uuid.uuid4(),
        task_id=task.id,
        user_id=user_id,
        can_edit=can_edit,
    )
    db.add(share)
    db.commit()
    db.refresh(share)
    return share


def remove_share(db: Session, task: Task, user_id: uuid.UUID) -> bool:
    share = (
        db.query(TaskShare)
        .filter(TaskShare.task_id == task.id, TaskShare.user_id == user_id)
        .first()
    )
    if not share:
        return False
    db.delete(share)
    db.commit()
    return True
