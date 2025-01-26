from pydantic import BaseModel

from models.messaging import MessageRole


class GPTMessageDto(BaseModel):
    role: MessageRole
    content: str
