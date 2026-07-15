import os

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from common.tokens.jwt_token_handler import JWTTokenHandler
from common.dates.date_delay_generator import DateDelayGenerator

jwt_secret_key = os.environ.get("JWT_SECRET_KEY", "default_jwt_secret_key")
jwt_algorithm = os.environ.get("JWT_ALGORITHM", "HS256")


@asynccontextmanager
async def lifespan_func(app: FastAPI):
    # 🚀 STARTUP
    app.state.jwt_handler = JWTTokenHandler(jwt_secret_key=jwt_secret_key, algorithm=jwt_algorithm)
    app.state.date_delay_generator = DateDelayGenerator()

    yield  # <- la app corre aquí

    # 🛑 SHUTDOWN
    print("Shutting down app")
    app.state.jwt_handler = None
