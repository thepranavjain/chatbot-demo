import os
import pytest

from sqlmodel import SQLModel, create_engine, Session

from models.messaging import MessageRole
from crud.messaging import (
    create_chat_session,
    get_chat_session_by_id,
    get_all_chat_sessions_by_user,
    delete_chat_session,
    update_chat_session,
    create_message,
    get_messages_by_session,
    get_message_by_id,
    update_message,
    delete_message,
)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///test.db",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


# Modify add_and_commit function to use the testing DB
def add_and_commit(db_session, instance):
    db_session.add(instance)
    db_session.commit()
    db_session.refresh(instance)
    return instance


def test_create_chat_session(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    assert chat_session.id is not None
    assert chat_session.name == "Test Session"
    assert chat_session.user_email == "test@example.com"


def test_get_chat_session_by_id(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    fetched_session = get_chat_session_by_id(session, chat_session.id)
    assert fetched_session.id == chat_session.id
    assert fetched_session.name == "Test Session"
    assert fetched_session.user_email == "test@example.com"


def test_get_all_chat_sessions_by_user(session):
    create_chat_session(session, name="Session 1", user_email="test@example.com")
    create_chat_session(session, name="Session 2", user_email="test@example.com")
    sessions = get_all_chat_sessions_by_user(session, "test@example.com")
    assert len(sessions) == 2
    assert sessions[0].name == "Session 2"
    assert sessions[1].name == "Session 1"


def test_delete_chat_session(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    delete_chat_session(session, chat_session)
    fetched_session = get_chat_session_by_id(session, chat_session.id)
    assert fetched_session is None


def test_update_chat_session(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    updated_session = update_chat_session(
        session, chat_session.id, name="Updated Session"
    )
    assert updated_session.name == "Updated Session"


def test_create_message(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    message = create_message(
        session, content="Hello", session_id=chat_session.id, role=MessageRole.USER
    )
    assert message.id is not None
    assert message.content == "Hello"
    assert message.session_id == chat_session.id
    assert message.role == MessageRole.USER


def test_get_messages_by_session(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    create_message(
        session, content="Hello", session_id=chat_session.id, role=MessageRole.USER
    )
    messages = get_messages_by_session(session, chat_session.id)
    assert len(messages) == 1
    assert messages[0].content == "Hello"


def test_get_message_by_id(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    message = create_message(
        session, content="Hello", session_id=chat_session.id, role=MessageRole.USER
    )
    fetched_message = get_message_by_id(session, message.id)
    assert fetched_message.id == message.id
    assert fetched_message.content == "Hello"


def test_update_message(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    message = create_message(
        session, content="Hello", session_id=chat_session.id, role=MessageRole.USER
    )
    updated_message = update_message(session, message, content="Updated Hello")
    assert updated_message.content == "Updated Hello"


def test_delete_message(session):
    chat_session = create_chat_session(
        session, name="Test Session", user_email="test@example.com"
    )
    message = create_message(
        session, content="Hello", session_id=chat_session.id, role=MessageRole.USER
    )
    delete_message(session, message)
    fetched_message = get_message_by_id(session, message.id)
    assert fetched_message is None


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
