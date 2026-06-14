from dotenv import load_dotenv
from fastapi import FastAPI
from routers import auth_router
from routers import chat_router

load_dotenv()

app = FastAPI(lifespan=chat_router.lifespan)

app.include_router(auth_router.router)

