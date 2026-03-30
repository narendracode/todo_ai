from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.base import Base  # noqa: F401 — ensures models register


def get_engine(database_url: str):
    return create_engine(database_url, echo=False)


def get_session_factory(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
