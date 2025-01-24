from sqlmodel import Session as DbSession, select

from db.utils import add_and_commit
from dto.messaging import MessageRole
from models.messaging import Message, ChatSession


def create_message(
    dbSession: DbSession, content: str, session_id: int, role: MessageRole
):
    new_message = Message(content=content, session_id=session_id, role=role)
    new_message = add_and_commit(dbSession, new_message)
    return new_message


def create_chat_session(dbSession: DbSession, name: str):
    new_session = ChatSession(name=name)
    new_session = add_and_commit(dbSession, new_session)
    return new_session


def get_chat_session_by_id(dbSession: DbSession, session_id: str):
    return dbSession.get(ChatSession, session_id)


def get_all_messages_by_session(dbSession: DbSession, session_id: int):
    return dbSession.exec(select(Message).where(Message.session_id == session_id)).all()
