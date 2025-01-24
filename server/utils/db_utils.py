from datetime import datetime
from typing import TypeVar

from sqlmodel import Session, SQLModel, Field
from sqlalchemy import Column, Integer, DateTime, func, Enum as SQLAlchemyEnum

from core.db import engine


def init_db():
    SQLModel.metadata.create_all(engine)


T = TypeVar("T")


def add_and_commit(db_session: Session, instance: T):
    db_session.add(instance)
    db_session.commit()
    db_session.refresh(instance)
    return instance


class AutoIncrementIdMixin:
    id: int = Field(primary_key=True)


class TimestampMixin:
    created: datetime = Field(nullable=False, default_factory=func.now)
    updated: datetime = Field(
        nullable=False,
        default_factory=func.now,
        sa_column_kwargs={"onupdate": func.now()},
    )
