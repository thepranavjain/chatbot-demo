import pytest
from unittest.mock import AsyncMock, call, MagicMock, patch
from pydantic import BaseModel

from fastapi import HTTPException
from sqlmodel import Session

from dto.messaging import MessageInput, UpdateMessageInput
from models.messaging import Message
from tests.utils.factory import (
    getMockChatSession,
    getMockUserMessage,
    getMockSystemMessage,
)

from service.messaging import (
    get_chat_sessions_by_user,
    remove_chat_session,
    update_chat_session_name,
    send_message,
    get_messages_by_session,
    update_message,
    remove_message,
)


class UserFactory(BaseModel):
    email: str


@pytest.fixture
def user():
    return UserFactory(email="test@example.com")


@pytest.fixture
def db_session():
    return MagicMock(spec=Session)


@pytest.mark.asyncio
@patch("service.messaging.chat", new_callable=AsyncMock, return_value="Hi there!")
@patch("service.messaging.get_messages_by_session_crud")
@patch("service.messaging.create_message")
@patch("service.messaging.create_chat_session")
@patch("asyncio.create_task")
async def test_send_message_creates_new_session(
    mock_create_task,
    mock_create_chat_session,
    mock_create_message,
    mock_get_messages_by_session_crud,
    mock_chat,
    user,
    db_session,
):
    message_input = MessageInput(content="Hello", session_id=None)
    new_chat_session = getMockChatSession(id=1, user_email=user.email)
    mock_create_chat_session.return_value = new_chat_session

    user_message = getMockUserMessage(id=1, session_id=1, content="Hello")
    gpt_reply = getMockSystemMessage(id=2, session_id=1, content="Hi there!")
    mock_create_message.side_effect = [user_message, gpt_reply]
    mock_get_messages_by_session_crud.return_value = [user_message]

    response = await send_message(message_input, user, db_session)

    mock_create_task.assert_called_once()
    assert mock_create_chat_session.call_args == call(
        db_session,
        name=mock_create_chat_session.call_args[1]["name"],
        user_email=user.email,
    )
    assert mock_get_messages_by_session_crud.call_args == call(
        db_session, session_id=1, limit=20, order_by="desc"
    )
    assert mock_chat.call_args == call([user_message])
    assert response.user_message.content == "Hello"
    assert response.user_message.session_id == 1
    assert response.reply.content == "Hi there!"
    assert response.reply.session_id == 1
    assert mock_create_message.call_count == 2


@pytest.mark.asyncio
@patch("service.messaging.chat", new_callable=AsyncMock, return_value="Hi there!")
@patch("service.messaging.get_messages_by_session_crud")
@patch("service.messaging.create_message")
@patch("service.messaging.get_chat_session_by_id")
async def test_send_message_existing_session(
    mock_get_chat_session_by_id,
    mock_create_message,
    mock_get_messages_by_session_crud,
    mock_chat,
    user,
    db_session,
):
    message_input = MessageInput(content="Hello", session_id=1)
    new_chat_session = getMockChatSession(id=1, user_email=user.email)
    mock_get_chat_session_by_id.return_value = new_chat_session

    user_message = getMockUserMessage(id=1, session_id=1, content="Hello")
    gpt_reply = getMockSystemMessage(id=2, session_id=1, content="Hi there!")
    mock_create_message.side_effect = [user_message, gpt_reply]
    mock_get_messages_by_session_crud.return_value = [user_message]

    response = await send_message(message_input, user, db_session)

    assert mock_get_chat_session_by_id.call_args == call(db_session, 1)
    assert mock_get_messages_by_session_crud.call_args == call(
        db_session, session_id=1, limit=20, order_by="desc"
    )
    assert mock_chat.call_args == call([user_message])
    assert response.user_message.content == "Hello"
    assert response.user_message.session_id == 1
    assert response.reply.content == "Hi there!"
    assert response.reply.session_id == 1
    assert mock_create_message.call_count == 2


@patch("service.messaging.get_all_chat_sessions_by_user")
def test_get_chat_sessions_by_user(
    mock_get_all_chat_sessions_by_user, user, db_session
):
    mock_chat_sessions = [
        getMockChatSession(id=1, user_email=user.email),
        getMockChatSession(id=2, user_email=user.email),
    ]
    mock_get_all_chat_sessions_by_user.return_value = mock_chat_sessions
    sessions = get_chat_sessions_by_user(user, db_session)
    assert sessions == mock_chat_sessions


@patch("service.messaging.delete_chat_session")
@patch("service.messaging.get_chat_session_by_id")
def test_remove_chat_session(
    mock_get_chat_session_by_id, mock_delete_chat_session, user, db_session
):
    chat_session = getMockChatSession(email=user.email)
    mock_get_chat_session_by_id.return_value = chat_session

    remove_chat_session(1, user, db_session)

    mock_get_chat_session_by_id.call_args == call(db_session, 1)
    mock_delete_chat_session.call_args == call(db_session, chat_session)


@patch("service.messaging.delete_chat_session")
@patch("service.messaging.get_chat_session_by_id")
def test_remove_unauthorized_chat_session(
    mock_get_chat_session_by_id, mock_delete_chat_session, user, db_session
):
    chat_session = getMockChatSession(user_email="incorrect@example.com")
    mock_get_chat_session_by_id.return_value = chat_session

    with pytest.raises(HTTPException) as exc_info:
        remove_chat_session(1, user, db_session)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Chat session not found"

    mock_get_chat_session_by_id.call_args == call(db_session, 1)
    mock_delete_chat_session.assert_not_called()


@patch("service.messaging.get_chat_session_by_id", return_value=None)
def test_remove_chat_session_not_found(mock_get_chat_session_by_id, user, db_session):
    with pytest.raises(HTTPException):
        remove_chat_session(1, user, db_session)


@pytest.mark.asyncio
@patch(
    "service.messaging.get_chat_topic", new_callable=AsyncMock, return_value="New Topic"
)
@patch("service.messaging.update_chat_session")
@patch("service.messaging.get_session")
async def test_update_chat_session_name(
    mock_get_session, mock_update_chat_session, mock_get_chat_topic
):
    messages = [MagicMock(spec=Message)]
    chat_session_id = 1

    mock_db_session = AsyncMock()

    async def mock_get_session():
        class AsyncContextManager:
            async def __aenter__(self):
                return mock_db_session

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                pass

        return AsyncContextManager()

    mock_get_session.return_value = mock_db_session

    await update_chat_session_name(messages, chat_session_id)

    mock_get_chat_topic.assert_called_once_with(messages)
    mock_update_chat_session.assert_called_once()


@patch("service.messaging.get_chat_session_by_id")
@patch("service.messaging.get_messages_by_session_crud")
def test_get_messages_by_session(
    mock_get_messages_by_session_crud, mock_get_chat_session_by_id, user, db_session
):
    chat_session = getMockChatSession(id=1, user_email=user.email)
    mock_get_chat_session_by_id.return_value = chat_session

    messages = [[getMockUserMessage(id=1, session_id=1, content="Hello")]]
    mock_get_messages_by_session_crud.return_value = messages

    response = get_messages_by_session(1, user, db_session)
    assert response == messages


@patch("service.messaging.get_chat_session_by_id")
@patch("service.messaging.get_messages_by_session_crud")
def test_get_messages_by_session_unauthorized(
    mock_get_messages_by_session_crud, mock_get_chat_session_by_id, user, db_session
):
    chat_session = getMockChatSession(id=1, user_email="incorrect@example.com")
    mock_get_chat_session_by_id.return_value = chat_session

    messages = [[getMockUserMessage(id=1, session_id=1, content="Hello")]]
    mock_get_messages_by_session_crud.return_value = messages

    with pytest.raises(HTTPException) as exc_info:
        get_messages_by_session(1, user, db_session)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Chat session not found"


@patch("service.messaging.update_message_crud")
@patch("service.messaging.get_message_by_id")
def test_update_message(
    mock_get_message_by_id, mock_update_message_crud, user, db_session
):
    message = getMockUserMessage(id=1, session_id=1, content="Hello")
    message.session = getMockChatSession(id=1, user_email=user.email)
    payload = UpdateMessageInput(content="Updated content")
    updated_message = getMockUserMessage(id=1, session_id=1, content="Updated content")

    mock_get_message_by_id.return_value = message
    mock_update_message_crud.return_value = updated_message

    response = update_message(1, payload, user, db_session)
    assert response == updated_message


@patch("service.messaging.update_message_crud")
@patch("service.messaging.get_message_by_id")
def test_update_message_unauthorized(
    mock_get_message_by_id, mock_update_message_crud, user, db_session
):
    message = getMockUserMessage(id=1, session_id=1, content="Hello")
    message.session = getMockChatSession(id=1, user_email="incorrect@example.com")
    payload = UpdateMessageInput(content="Updated content")
    updated_message = getMockUserMessage(id=1, session_id=1, content="Updated content")

    mock_get_message_by_id.return_value = message
    mock_update_message_crud.return_value = updated_message

    with pytest.raises(HTTPException) as exc_info:
        update_message(1, payload, user, db_session)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Message not found"


@patch("service.messaging.delete_message")
@patch("service.messaging.get_message_by_id")
def test_remove_message(mock_get_message_by_id, mock_delete_message, user, db_session):
    message = getMockUserMessage(id=1, session_id=1, content="Hello")
    message.session = getMockChatSession(id=1, user_email=user.email)

    mock_get_message_by_id.return_value = message

    remove_message(1, user, db_session)
    mock_delete_message.assert_called_once_with(db_session, message)


def test_remove_message_not_found(user, db_session):
    with patch("service.messaging.get_message_by_id", return_value=None):
        with pytest.raises(HTTPException):
            remove_message(1, user, db_session)
