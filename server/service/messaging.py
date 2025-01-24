from datetime import datetime
from logging import getLogger

from fastapi import HTTPException
from firebase_admin.auth import UserRecord
from sqlmodel import Session

from dto.messaging import MessageInput, SendMessageRes, UpdateMessageInput
from crud.messaging import (
    create_message,
    create_chat_session,
    get_all_chat_sessions_by_user,
    get_chat_session_by_id,
    get_message_by_id,
    get_messages_by_session as get_messages_by_session_crud,
    update_chat_session,
    update_message as update_message_crud,
    delete_message,
    delete_chat_session,
)
from models.messaging import MessageRole
from service.gpt import chat, get_chat_topic


CHAT_HISTORY_LIMIT = 20

logger = getLogger()


def get_chat_sessions_by_user(user: UserRecord, dbSession: Session):
    return get_all_chat_sessions_by_user(dbSession, user.email)


def remove_chat_session(session_id: int, user: UserRecord, dbSession: Session):
    chat_session = get_chat_session_by_id(dbSession, session_id)
    if not chat_session or chat_session.user_email != user.email:
        raise HTTPException(status_code=404, detail="Chat session not found")
    delete_chat_session(dbSession, chat_session)


async def send_message(message: MessageInput, user: UserRecord, dbSession: Session):
    new_session_created = False
    if not message.session_id:
        new_session = create_chat_session(
            dbSession, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user.email
        )
        message.session_id = new_session.id
        new_session_created = True
    else:
        chat_session = get_chat_session_by_id(dbSession, message.session_id)
        if chat_session.user_email != user.email or not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")

    user_message = create_message(
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

    if new_session_created:
        try:
            chat_topic = await get_chat_topic([user_message, reply])
            update_chat_session(dbSession, user_message.session_id, name=chat_topic)
        except Exception as e:
            logger.error(f"Failed to update chat session with topic: {e}")

    return SendMessageRes(user_message=user_message, reply=reply)


def get_messages_by_session(session_id: int, user: UserRecord, dbSession: Session):
    chat_session = get_chat_session_by_id(dbSession, session_id)
    if chat_session.user_email != user.email or not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return get_messages_by_session_crud(dbSession, session_id=session_id)


def update_message(
    message_id: int, payload: UpdateMessageInput, user: UserRecord, dbSession: Session
):
    message = get_message_by_id(dbSession, message_id)
    if not message or message.session.user_email != user.email:
        raise HTTPException(status_code=404, detail="Message not found")
    message = update_message_crud(dbSession, message, content=payload.content)
    return message


def remove_message(message_id: int, user: UserRecord, dbSession: Session):
    message = get_message_by_id(dbSession, message_id)
    if (
        not message
        or message.session.user_email != user.email
        or message.role is not MessageRole.USER
    ):
        raise HTTPException(status_code=404, detail="Message not found")
    delete_message(dbSession, message)
