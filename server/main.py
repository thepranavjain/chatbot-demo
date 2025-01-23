from fastapi import FastAPI

from db.utils import add_and_commit, init_db, DbSessionDep
from models.message import Session, Message, MessageInput, MessageRole


router = FastAPI()

print("Initializing database...")
init_db()
print("Database initialized.")


@router.post("/message", response_model=Message)
async def send_message(message: MessageInput, dbSession: DbSessionDep):
    if not message.session_id:
        new_session = Session(name="New Session")
        new_session = add_and_commit(dbSession, new_session)
        message.session_id = new_session.id

    new_message = Message(
        content=message.content, session_id=message.session_id, role=MessageRole.USER
    )
    new_message = add_and_commit(dbSession, new_message)

    reply = Message(
        content="Reply from system here",
        session_id=message.session_id,
        role=MessageRole.SYSTEM,
    )
    reply = add_and_commit(dbSession, reply)

    return reply
