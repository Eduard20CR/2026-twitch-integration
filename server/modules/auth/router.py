import os

from fastapi import APIRouter, Depends, Request, HTTPException

from modules.auth.infrastructure.twitch_api_client import TwitchApiClient
from modules.auth.infrastructure.twitch_auth_client import TwitchAuthClient
from common.tokens.refresh_token_handler import RefreshTokenHandler
from common.tokens.jwt_token_handler import JWTTokenHandler
from common.dates.date_delay_generator import DateDelayGenerator
from common.factories.auh_redirect_factory import RedirectFactory
from common.factories.auth_cookie_factory import CookieFactory
from common.dependencies.get_current_user import get_current_user

from .services.auth_service import AuthService
from .controller import AuthController
from .domain.exceptions import OAuthException

twitch_redirect_url = os.getenv("TWITCH_REDIRECT_URL")
twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
frontend_url = os.getenv("FRONTEND_URL")
jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")

date_delay_generator = DateDelayGenerator()
refresh_token_handler = RefreshTokenHandler()
jwt_token_handler = JWTTokenHandler(jwt_secret_key=jwt_secret_key, algorithm=jwt_algorithm)
twitch_auth_client = TwitchAuthClient(client_id=twitch_client_id)
twitch_api_client = TwitchApiClient(client_id=twitch_client_id)
redirect_factory = RedirectFactory()
cookie_factory = CookieFactory()

auth_service = AuthService(
    twitch_auth_client=twitch_auth_client,
    twitch_api_client=twitch_api_client,
    refresh_token_handler=refresh_token_handler,
    jwt_token_handler=jwt_token_handler,
    date_delay_generator=date_delay_generator,
    redirect_url=twitch_redirect_url,
)
auth_controller = AuthController(
    service=auth_service, redirect_factory=redirect_factory, cookie_factory=cookie_factory, frontend_url=frontend_url
)

auth_router = APIRouter(prefix="/api/auth")


@auth_router.get("/login")
async def login(request: Request):
    return await auth_controller.login(request)


@auth_router.get("/callback")
async def callback(request: Request):
    try:
        return await auth_controller.callback(request)
    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")


@auth_router.get("/me")
async def me(current_user=Depends(get_current_user)):
    print("Current user:", current_user)
    return current_user
