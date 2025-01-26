from core.openai import async_openai_client
from dto.gpt import GPTMessageDto


async def chat(messages: list[GPTMessageDto]):
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


async def get_chat_topic(messages: list[GPTMessageDto]):
    gpt_messages = [
        *[
            {"role": messageEntity.role.value.lower(), "content": messageEntity.content}
            for messageEntity in messages
        ],
        {
            "role": "system",
            "content": "You are a helpful chatbot assistant. These are the first few messages of a given chat session. Get chat topic. Just a brief topic name in plaintext. No extra text.",
        },
    ]
    response = await async_openai_client.chat.completions.create(
        messages=gpt_messages, model="gpt-3.5-turbo"
    )
    return response.choices[0].message.content
