from typing import Annotated, TypeVar

from fastapi import Depends
from sqlmodel import Session, SQLModel

from core.db import engine


def init_db():
    SQLModel.metadata.create_all(engine)


T = TypeVar("T")


def add_and_commit(db_session: Session, instance: T):
    db_session.add(instance)
    db_session.commit()
    db_session.refresh(instance)
    return instance
