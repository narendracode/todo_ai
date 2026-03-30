from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todoai_common.schemas.auth import (
    AccessTokenResponse,
    GoogleAuthRequest,
    RefreshRequest,
    TokenResponse,
)
from todoai_common.schemas.user import UserOut

from ..dependencies import get_db
from ..services import auth_service

router = APIRouter()


@router.post("/google", response_model=TokenResponse)
async def google_auth(body: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        google_data = await auth_service.verify_google_id_token(body.id_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user = auth_service.upsert_user(db, google_data)
    user_id = str(user.id)
    return TokenResponse(
        access_token=auth_service.create_access_token(user_id),
        refresh_token=auth_service.create_refresh_token(user_id),
    )


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh_token(body: RefreshRequest):
    try:
        user_id = auth_service.decode_refresh_token(body.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return AccessTokenResponse(access_token=auth_service.create_access_token(user_id))
