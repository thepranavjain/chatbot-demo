from typing import Annotated, TypeVar

from fastapi import Depends
from sqlmodel import Session, SQLModel

from .db import engine


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


DbSessionDependency = Annotated[Session, Depends(get_session)]


T = TypeVar("T")


def add_and_commit(db_session: Session, instance: T):
    db_session.add(instance)
    db_session.commit()
    db_session.refresh(instance)
    return instance
