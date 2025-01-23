from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, Integer, Enum as SQLAlchemyEnum


class MessageRole(Enum):
    USER = "user"
    SYSTEM = "system"


class Session(SQLModel, table=True):
    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    name: str | None
    messages: list["Message"] = Relationship(back_populates="session")


class MessageBase(SQLModel):
    content: str


class MessageInput(MessageBase):
    session_id: int | None = None


class Message(MessageBase, table=True):
    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    session_id: int = Field(foreign_key="session.id")
    session: Session = Relationship(back_populates="messages")
    role: MessageRole = Field(sa_column=Column(SQLAlchemyEnum(MessageRole)))


# Resolve forward references
Session.__annotations__["messages"] = list[Message]
Message.__annotations__["session"] = Session
