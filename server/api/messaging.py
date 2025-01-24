from fastapi import APIRouter, Depends
from firebase_admin.auth import UserRecord

from dependencies.auth import firebase_auth_dependency
from dependencies.db import DbSessionDependency
from dto.messaging import MessageInput
from models.messaging import ChatSession, Message
from service.messaging import (
    send_message,
    get_messages_by_session,
    get_chat_sessions_by_user,
)


from fastapi import Security
from fastapi.security import HTTPBearer


security_scheme = HTTPBearer()

messaging_router = APIRouter(
    dependencies=[Depends(firebase_auth_dependency), Security(security_scheme)]
)


@messaging_router.post("/message", response_model=Message)
async def post_message(
    message: MessageInput,
    dbSession: DbSessionDependency,
    user: UserRecord = Depends(firebase_auth_dependency),
):
    return await send_message(message, user, dbSession)


@messaging_router.get("/chat-session", response_model=list[ChatSession])
async def get_chat_sessions(
    dbSession: DbSessionDependency, user: UserRecord = Depends(firebase_auth_dependency)
):
    return get_chat_sessions_by_user(user, dbSession)


@messaging_router.get(
    "/chat-session/messages/{session_id}", response_model=list[Message]
)
async def get_session_messages(
    session_id: int,
    dbSession: DbSessionDependency,
    user: UserRecord = Depends(firebase_auth_dependency),
):
    return get_messages_by_session(session_id, user, dbSession)
