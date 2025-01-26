from datetime import datetime
from unittest.mock import MagicMock

from models.messaging import ChatSession, Message, MessageRole


def getMockChatSession(**kwargs):
    chat_session = MagicMock(spec=ChatSession)
    chat_session.id = kwargs.get("id", 1)
    chat_session.user_email = kwargs.get("user_email", "test@example.com")
    return chat_session


def getMockChatMessage(**kwargs):
    message = MagicMock(spec=Message)
    message.id = kwargs.get("id", 1)
    message.content = kwargs.get("content", "Hello")
    message.session_id = kwargs.get("session_id", 1)
    message.role = kwargs.get("role", MessageRole.USER)
    message.created = kwargs.get("created", datetime.now())
    message.updated = kwargs.get("updated", datetime.now())
    return message


def getMockUserMessage(**kwargs):
    return getMockChatMessage(role=MessageRole.USER, **kwargs)


def getMockSystemMessage(**kwargs):
    return getMockChatMessage(role=MessageRole.SYSTEM, **kwargs)
