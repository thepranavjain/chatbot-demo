from sqlmodel import Session as DbSession, select, delete

from models.messaging import Message, ChatSession, MessageRole
from utils.db_utils import add_and_commit


def create_chat_session(dbSession: DbSession, name: str, user_email: str):
    new_session = ChatSession(name=name, user_email=user_email)
    new_session = add_and_commit(dbSession, new_session)
    return new_session


def get_chat_session_by_id(dbSession: DbSession, session_id: str):
    return dbSession.get(ChatSession, session_id)


def get_all_chat_sessions_by_user(dbSession: DbSession, user_email: str):
    return dbSession.exec(
        select(ChatSession)
        .where(ChatSession.user_email == user_email)
        .order_by(ChatSession.id.desc())
    ).all()


def delete_chat_session(dbSession: DbSession, session: ChatSession):
    if session:
        dbSession.exec(delete(Message).where(Message.session_id == session.id))
        dbSession.delete(session)
        dbSession.commit()


def update_chat_session(
    dbSession: DbSession, session_id: int, name: str = None, user_email: str = None
):
    session = dbSession.get(ChatSession, session_id)
    if session:
        if name is not None:
            session.name = name
        if user_email is not None:
            session.user_email = user_email
        session = add_and_commit(session)
    return session


def create_message(
    dbSession: DbSession, content: str, session_id: int, role: MessageRole
):
    new_message = Message(content=content, session_id=session_id, role=role)
    new_message = add_and_commit(dbSession, new_message)
    return new_message


def get_messages_by_session(
    dbSession: DbSession,
    session_id: int,
    limit: int | None = None,
    offset: int | None = None,
):
    query = (
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.id.desc())
    )
    if limit != None:
        query.limit(limit)
    if offset != None:
        query.offset(offset)
    return dbSession.exec(query).all()


def get_message_by_id(dbSession: DbSession, message_id: int):
    message = dbSession.get(Message, message_id)
    if message:
        message.session = dbSession.get(ChatSession, message.session_id)
    return message


def update_message(dbSession: DbSession, message: Message, content: str = None):
    if content is not None:
        message.content = content
    message = add_and_commit(dbSession, message)
    return message


def delete_message(dbSession: DbSession, message: Message):
    if message:
        dbSession.delete(message)
        dbSession.commit()
