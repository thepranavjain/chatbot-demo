import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from service.gpt import chat, get_chat_topic
from dto.gpt import GPTMessageDto, MessageRole


@pytest.fixture
def mock_async_openai_client():
    with patch("service.gpt.async_openai_client") as mock_client:
        mock_client.chat.completions.create = AsyncMock()
        yield mock_client


@pytest.mark.asyncio
async def test_chat(mock_async_openai_client):
    mock_response = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Mocked response"))]
    )
    mock_async_openai_client.chat.completions.create.return_value = mock_response

    messages = [GPTMessageDto(role=MessageRole.USER, content="Hello")]
    response = await chat(messages)

    assert response == "Mocked response"
    mock_async_openai_client.chat.completions.create.assert_called_once_with(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful chatbot assistant. Following are the most recent messages of a given chat session.",
            },
            {"role": "user", "content": "Hello"},
        ],
        model="gpt-3.5-turbo",
    )


@pytest.mark.asyncio
async def test_get_chat_topic(mock_async_openai_client):
    mock_response = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Mocked topic"))]
    )
    mock_async_openai_client.chat.completions.create.return_value = mock_response

    messages = [GPTMessageDto(role=MessageRole.USER, content="Hello")]
    response = await get_chat_topic(messages)

    assert response == "Mocked topic"
    mock_async_openai_client.chat.completions.create.assert_called_once_with(
        messages=[
            {"role": "user", "content": "Hello"},
            {
                "role": "system",
                "content": "You are a helpful chatbot assistant. These are the first few messages of a given chat session. Get chat topic. Just a brief topic name in plaintext. No extra text.",
            },
        ],
        model="gpt-3.5-turbo",
    )
