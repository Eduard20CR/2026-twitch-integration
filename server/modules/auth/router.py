import os

from fastapi import APIRouter, Request, HTTPException

from modules.auth.infrastructure.twitch_api_client import TwitchApiClient
from modules.auth.infrastructure.twitch_auth_client import TwitchAuthClient

from .services.auth_service import AuthService
from .controller import AuthController
from .domain.exceptions import OAuthException

twitch_redirect_url = os.getenv("TWITCH_REDIRECT_URL")
twitch_client_id = os.getenv("TWITCH_CLIENT_ID")

twitch_auth_client = TwitchAuthClient(client_id=twitch_client_id)
twitch_api_client = TwitchApiClient(client_id=twitch_client_id)
auth_service = AuthService(
    twitch_auth_client=twitch_auth_client,
    twitch_api_client=twitch_api_client,
    redirect_url=twitch_redirect_url,
)
auth_controller = AuthController(service=auth_service)

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/login")
async def login(request: Request):
    return await auth_controller.login(request)


@auth_router.get("/callback")
async def callback(request: Request):
    try:
        return await auth_controller.callback(request)
    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")
