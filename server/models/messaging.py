from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, Integer, Enum as SQLAlchemyEnum

from dto.messaging import MessageRole
from utils.db_utils import AutoIncrementIdMixin, TimestampMixin


class ChatSession(AutoIncrementIdMixin, TimestampMixin, SQLModel, table=True):
    name: str | None
    user_email: str
    messages: list["Message"] = Relationship(back_populates="session")


class Message(AutoIncrementIdMixin, TimestampMixin, SQLModel, table=True):
    content: str
    role: MessageRole = Field(sa_column=Column(SQLAlchemyEnum(MessageRole)))
    session_id: int = Field(foreign_key="chatsession.id")
    session: ChatSession = Relationship(back_populates="messages")


# Resolve forward references
ChatSession.__annotations__["messages"] = list[Message]
Message.__annotations__["session"] = ChatSession
