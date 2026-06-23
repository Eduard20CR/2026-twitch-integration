import os

from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware

from fastapi import FastAPI
from modules.auth.router import auth_router
from modules.chat.router import chat_router, lifespan

load_dotenv()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("AUTH_SESSION_SECRET_KEY", "default_secret_key"),
)

app.include_router(auth_router)
