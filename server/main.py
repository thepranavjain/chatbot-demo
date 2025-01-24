from logging import getLogger

from fastapi import FastAPI

from db.utils import init_db
from api.messaging import messaging_router


router = FastAPI()

logger = getLogger()

logger.info("Initializing database...")
init_db()
logger.info("Database initialized.")

router.include_router(messaging_router, prefix="/messaging")
