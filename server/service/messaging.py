from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session

from dto.messaging import MessageInput, MessageRole
from crud.messaging import (
    create_message,
    create_chat_session,
    get_all_messages_by_session,
    get_chat_session_by_id,
)


def send_message(message: MessageInput, dbSession: Session):
    if not message.session_id:
        new_session = create_chat_session(
            dbSession, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        message.session_id = new_session.id
    else:
        chat_session = get_chat_session_by_id(dbSession, message.session_id)
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")

    create_message(
        dbSession,
        content=message.content,
        session_id=message.session_id,
        role=MessageRole.USER,
    )

    reply = create_message(
        dbSession,
        content="Reply from system here",
        session_id=message.session_id,
        role=MessageRole.SYSTEM,
    )

    return reply


def get_messages_by_session(session_id: int, dbSession: Session):
    chat_session = get_chat_session_by_id(dbSession, session_id)
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return get_all_messages_by_session(dbSession, session_id=session_id)
