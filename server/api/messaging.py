from fastapi import APIRouter

from core.utils import DbSessionDependency
from dto.messaging import MessageInput
from models.messaging import Message
from service.messaging import send_message, get_messages_by_session

messaging_router = APIRouter()


@messaging_router.post("/message", response_model=Message)
async def post_message(message: MessageInput, dbSession: DbSessionDependency):
    return await send_message(message, dbSession)


@messaging_router.get("/session/messages/{session_id}", response_model=list[Message])
async def get_session_messages(session_id: int, dbSession: DbSessionDependency):
    return get_messages_by_session(session_id, dbSession)
