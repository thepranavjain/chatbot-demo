from dotenv import load_dotenv

# Load up env vars from .env
load_dotenv()

from logging import getLogger

logger = getLogger()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import initialize_app as initialize_firebase_app

from api.messaging import messaging_router
from core.firebase import firebase_cred
from utils.db_utils import init_db


initialize_firebase_app(firebase_cred)

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

logger.info("Initializing database...")
init_db()
logger.info("Database initialized.")

app.include_router(messaging_router, prefix="/messaging")
