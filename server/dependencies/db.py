from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.db import engine


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


DbSessionDependency = Annotated[Session, Depends(get_session)]
