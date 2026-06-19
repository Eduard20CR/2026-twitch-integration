import os

from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware

from fastapi import FastAPI
from routers import auth_router
from routers import chat_router

load_dotenv()

app = FastAPI(lifespan=chat_router.lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SESSION_SECRET_KEY", "default_secret_key"),
)

app.include_router(auth_router.router)
