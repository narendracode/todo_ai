import logging
import uuid
from datetime import datetime, timedelta, timezone

import httpx
from jose import jwt
from sqlalchemy.orm import Session

from todoai_common.models import User

from ..config import settings

logger = logging.getLogger(__name__)


async def verify_google_id_token(id_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
        )
    if resp.status_code != 200:
        logger.error("Google tokeninfo rejected the token: %s — %s", resp.status_code, resp.text)
        raise ValueError("Invalid Google id_token")

    data = resp.json()
    token_aud = data.get("aud") or data.get("azp")  # azp is fallback for some Google tokens

    if token_aud != settings.google_client_id:
        logger.error(
            "Audience mismatch — token aud=%r, GOOGLE_CLIENT_ID=%r. "
            "Make sure api/.env GOOGLE_CLIENT_ID matches AUTH_GOOGLE_ID in frontend .env.local",
            token_aud,
            settings.google_client_id,
        )
        raise ValueError(
            f"Token audience mismatch: got {token_aud!r}, expected {settings.google_client_id!r}"
        )
    return data


def upsert_user(db: Session, google_data: dict) -> User:
    google_sub = google_data["sub"]
    user = db.query(User).filter(User.google_sub == google_sub).first()
    if user is None:
        user = User(
            id=uuid.uuid4(),
            google_sub=google_sub,
            email=google_data["email"],
            name=google_data.get("name", google_data["email"]),
            avatar_url=google_data.get("picture"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.name = google_data.get("name", user.name)
        user.avatar_url = google_data.get("picture", user.avatar_url)
        db.commit()
        db.refresh(user)
    return user


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(
        {"sub": user_id, "type": "access", "exp": expire},
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    return jwt.encode(
        {"sub": user_id, "type": "refresh", "exp": expire},
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_refresh_token(token: str) -> str:
    from jose import JWTError

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise ValueError("Not a refresh token")
        return payload["sub"]
    except JWTError as e:
        raise ValueError(f"Invalid refresh token: {e}")
