from os import environ

from openai import AsyncOpenAI


async_openai_client = AsyncOpenAI(
    api_key=environ.get("OPENAI_API_KEY", "api-key-unavailable")
)
