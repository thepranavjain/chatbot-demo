from datetime import datetime

from fastapi import HTTPException
from firebase_admin.auth import UserRecord
from sqlmodel import Session

from dto.messaging import MessageInput, MessageRole
from crud.messaging import (
    create_message,
    create_chat_session,
    get_all_messages_by_session,
    get_chat_session_by_id,
    get_messages_by_session as get_messages_by_session_crud,
)
from service.gpt import chat


CHAT_HISTORY_LIMIT = 20


async def send_message(message: MessageInput, user: UserRecord, dbSession: Session):
    if not message.session_id:
        new_session = create_chat_session(
            dbSession, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user.email
        )
        message.session_id = new_session.id
    else:
        chat_session = get_chat_session_by_id(dbSession, message.session_id)
        if chat_session.user_email != user.email or not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")

    create_message(
        dbSession,
        content=message.content,
        session_id=message.session_id,
        role=MessageRole.USER,
    )

    recent_messages = get_messages_by_session_crud(
        dbSession, session_id=message.session_id, limit=CHAT_HISTORY_LIMIT
    )  # These are sorted by latest first
    gpt_reply = await chat(list(reversed(recent_messages)))

    reply = create_message(
        dbSession,
        content=gpt_reply,
        session_id=message.session_id,
        role=MessageRole.SYSTEM,
    )

    return reply


def get_messages_by_session(session_id: int, user: UserRecord, dbSession: Session):
    chat_session = get_chat_session_by_id(dbSession, session_id)
    if chat_session.user_email != user.email or not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return get_all_messages_by_session(dbSession, session_id=session_id)
