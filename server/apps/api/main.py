from dotenv import load_dotenv

load_dotenv()

import os


from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from modules.auth.router import auth_router
from modules.chat.router import chat_router
from common.lifespan import lifespan

app = FastAPI(lifespan=lifespan.lifespan_func)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("AUTH_SESSION_SECRET_KEY", "default_secret_key"),
)

app.include_router(auth_router)
app.include_router(chat_router)
