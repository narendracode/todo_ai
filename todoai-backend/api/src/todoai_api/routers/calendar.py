from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from todoai_common.models import User

from ..dependencies import get_current_user, get_db
from ..services import calendar_service

router = APIRouter()


@router.get("/events")
def get_events(
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return calendar_service.get_calendar_events(db, current_user, start, end)
