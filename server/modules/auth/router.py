import os

from fastapi import APIRouter, Request, HTTPException

from modules.auth.infrastructure.twitch_client import TwitchClient
from .service.service import AuthService
from .controller import AuthController
from .domain.exceptions import OAuthException

auth_router = APIRouter(prefix="/auth")

redirect_url = os.getenv("REDIRECT_URL")

twitch_client = TwitchClient()
auth_service = AuthService(twitch_client=twitch_client, redirect_url=redirect_url)
auth_controller = AuthController(service=auth_service)


@auth_router.get("/login")
async def login(request: Request):
    return await auth_controller.login(request)


@auth_router.get("/callback")
async def callback(request: Request):
    try:
        return await auth_controller.callback(request)
    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")
