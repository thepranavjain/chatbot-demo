from enum import Enum

from pydantic import BaseModel


class MessageRole(Enum):
    USER = "user"
    SYSTEM = "system"


class MessageInput(BaseModel):
    content: str
    session_id: int | None = None
