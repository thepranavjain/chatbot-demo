from fastapi import APIRouter, Depends
from firebase_admin.auth import UserRecord

from dependencies.auth import firebase_auth_dependency
from dependencies.db import DbSessionDependency
from dto.messaging import MessageInput, SendMessageRes, UpdateMessageInput
from models.messaging import ChatSession, Message
from service.messaging import (
    send_message,
    get_messages_by_session,
    get_chat_sessions_by_user,
    update_message,
    remove_chat_session,
    remove_message,
)


from fastapi import Security
from fastapi.security import HTTPBearer


security_scheme = HTTPBearer()

messaging_router = APIRouter(
    dependencies=[Depends(firebase_auth_dependency), Security(security_scheme)]
)


@messaging_router.post("/message", response_model=SendMessageRes)
async def post_message(
    message: MessageInput,
    dbSession: DbSessionDependency,
    user: UserRecord = Depends(firebase_auth_dependency),
):
    return await send_message(message, user, dbSession)


@messaging_router.patch("message/{message_id}", response_model=Message)
async def patch_message(
    message_id: int,
    payload: UpdateMessageInput,
    dbSession: DbSessionDependency,
    user: UserRecord = Depends(firebase_auth_dependency),
):
    return update_message(message_id, payload, user, dbSession)


@messaging_router.delete("message/{message_id}")
async def delete_message(
    message_id: int,
    dbSession: DbSessionDependency,
    user: UserRecord = Depends(firebase_auth_dependency),
):
    return remove_message(message_id, user, dbSession)


@messaging_router.get("/chat-session", response_model=list[ChatSession])
async def get_chat_sessions(
    dbSession: DbSessionDependency, user: UserRecord = Depends(firebase_auth_dependency)
):
    return get_chat_sessions_by_user(user, dbSession)


@messaging_router.get(
    "/chat-session/{session_id}/messages", response_model=list[Message]
)
async def get_session_messages(
    session_id: int,
    dbSession: DbSessionDependency,
    user: UserRecord = Depends(firebase_auth_dependency),
):
    return get_messages_by_session(session_id, user, dbSession)


@messaging_router.delete("chat-session/{session_id}")
async def delete_chat_session(
    session_id: int,
    dbSession: DbSessionDependency,
    user: UserRecord = Depends(firebase_auth_dependency),
):
    return remove_chat_session(session_id, user, dbSession)
