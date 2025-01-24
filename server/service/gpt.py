from core.openai import async_openai_client
from models.messaging import Message


async def chat(messages: list[Message]):
    gpt_messages = [
        {
            "role": "system",
            "content": "You are a helpful chatbot assistant. Following are the most recent messages of a given chat session.",
        }
    ]
    gpt_messages.extend(
        [
            {"role": messageEntity.role.value.lower(), "content": messageEntity.content}
            for messageEntity in messages
        ]
    )
    response = await async_openai_client.chat.completions.create(
        messages=gpt_messages, model="gpt-3.5-turbo"
    )
    return response.choices[0].message.content
