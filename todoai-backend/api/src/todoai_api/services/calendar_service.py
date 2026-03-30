from datetime import datetime

from dateutil.rrule import rrulestr
from sqlalchemy import or_
from sqlalchemy.orm import Session

from todoai_common.enums import Visibility
from todoai_common.models import Task, TaskShare, User

PRIORITY_COLORS = {
    "low": "#22c55e",
    "medium": "#3b82f6",
    "high": "#f97316",
    "urgent": "#ef4444",
}


def get_calendar_events(
    db: Session, user: User, start: datetime, end: datetime
) -> list[dict]:
    tasks = (
        db.query(Task)
        .filter(
            or_(
                Task.owner_id == user.id,
                Task.assigned_to_id == user.id,
                Task.visibility == Visibility.PUBLIC,
                Task.id.in_(
                    db.query(TaskShare.task_id).filter(TaskShare.user_id == user.id)
                ),
            ),
            or_(
                Task.time_from.between(start, end),
                Task.is_recurring == True,  # noqa: E712
            ),
        )
        .all()
    )

    events = []
    for task in tasks:
        if task.is_recurring and task.recurrence_rule and task.time_from:
            duration = None
            if task.time_to and task.time_from:
                duration = task.time_to - task.time_from
            try:
                rule = rrulestr(task.recurrence_rule, dtstart=task.time_from)
                occurrences = rule.between(start, end, inc=True)
                for occ in occurrences:
                    event_end = occ + duration if duration else occ
                    events.append(_build_event(task, occ, event_end))
            except Exception:
                pass
        elif task.time_from:
            events.append(_build_event(task, task.time_from, task.time_to or task.time_from))

    return events


def _build_event(task: Task, start: datetime, end: datetime) -> dict:
    return {
        "id": str(task.id),
        "title": task.title,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "allDay": False,
        "backgroundColor": PRIORITY_COLORS.get(task.priority.value, "#3b82f6"),
        "extendedProps": {
            "task_id": str(task.id),
            "priority": task.priority.value,
            "status": task.status.value,
            "is_recurring": task.is_recurring,
        },
    }
