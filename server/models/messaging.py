from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, Integer, Enum as SQLAlchemyEnum

from dto.messaging import MessageRole


class ChatSession(SQLModel, table=True):
    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    name: str | None
    messages: list["Message"] = Relationship(back_populates="session")


class Message(SQLModel, table=True):
    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    content: str
    session_id: int = Field(foreign_key="chatsession.id")
    session: ChatSession = Relationship(back_populates="messages")
    role: MessageRole = Field(sa_column=Column(SQLAlchemyEnum(MessageRole)))


# Resolve forward references
ChatSession.__annotations__["messages"] = list[Message]
Message.__annotations__["session"] = ChatSession
