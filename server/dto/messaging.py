from datetime import datetime

from pydantic import BaseModel

from models.messaging import MessageRole


# Assuming Message is defined like this
class Message(BaseModel):
    id: int
    content: str
    role: MessageRole
    session_id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True 


class MessageInput(BaseModel):
    content: str
    session_id: int | None = None


class UpdateMessageInput(BaseModel):
    content: str


class SendMessageRes(BaseModel):
    user_message: Message
    reply: Message
