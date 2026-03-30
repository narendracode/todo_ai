import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todoai_common.enums import Priority, TaskStatus
from todoai_common.models import User
from todoai_common.schemas.task import (
    PaginatedTasks,
    TaskCreate,
    TaskOut,
    TaskShareCreate,
    TaskShareOut,
    TaskUpdate,
)

from ..dependencies import get_current_user, get_db
from ..services import task_service

router = APIRouter()


@router.get("", response_model=PaginatedTasks)
def list_tasks(
    status: TaskStatus | None = None,
    priority: Priority | None = None,
    assigned_to: uuid.UUID | None = None,
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.list_tasks(db, current_user, status, priority, assigned_to, page, size)


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    body: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(db, current_user, body)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.get_task(db, current_user, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: uuid.UUID,
    body: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.get_task(db, current_user, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not task owner")
    return task_service.update_task(db, task, body)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.get_task(db, current_user, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not task owner")
    task_service.delete_task(db, task)


@router.post("/{task_id}/shares", response_model=TaskShareOut, status_code=status.HTTP_201_CREATED)
def add_share(
    task_id: uuid.UUID,
    body: TaskShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.get_task(db, current_user, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not task owner")
    return task_service.add_share(db, task, body.user_id, body.can_edit)


@router.delete("/{task_id}/shares/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_share(
    task_id: uuid.UUID,
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.get_task(db, current_user, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not task owner")
    if not task_service.remove_share(db, task, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Share not found")
