from dotenv import load_dotenv

# Load up env vars from .env
load_dotenv()

from logging import getLogger

logger = getLogger()

from fastapi import FastAPI

from core.utils import init_db
from api.messaging import messaging_router


router = FastAPI()


logger.info("Initializing database...")
init_db()
logger.info("Database initialized.")

router.include_router(messaging_router, prefix="/messaging")
