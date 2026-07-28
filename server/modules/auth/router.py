import os

from fastapi import APIRouter, Depends, Request, HTTPException, Response

from common.env.settings import settings
from common.security.encryption import EncryptionService
from modules.auth.infrastructure.twitch_api_client import TwitchApiClient
from modules.auth.infrastructure.twitch_auth_client import TwitchAuthClient
from common.tokens.refresh_token_handler import RefreshTokenHandler
from common.tokens.jwt_token_handler import JWTTokenHandler
from common.dates.date_delay_generator import DateDelayGenerator
from common.factories.auh_redirect_factory import RedirectFactory
from common.factories.auth_cookie_factory import CookieFactory
from common.dependencies.get_current_user import get_current_user
from common.dependencies.get_refresh_token import get_refresh_token

from .services.auth_service import AuthService
from .controller import AuthController
from .domain.exceptions import OAuthException

encryption_service = EncryptionService(key=settings.encryption_key)
date_delay_generator = DateDelayGenerator()
refresh_token_handler = RefreshTokenHandler()
jwt_token_handler = JWTTokenHandler(jwt_secret_key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
twitch_auth_client = TwitchAuthClient(client_id=settings.twitch_client_id)
twitch_api_client = TwitchApiClient(client_id=settings.twitch_client_id)
redirect_factory = RedirectFactory()
cookie_factory = CookieFactory()

auth_service = AuthService(
    twitch_auth_client=twitch_auth_client,
    twitch_api_client=twitch_api_client,
    refresh_token_handler=refresh_token_handler,
    jwt_token_handler=jwt_token_handler,
    date_delay_generator=date_delay_generator,
    encryption_service=encryption_service,
    redirect_url=settings.twitch_redirect_url,
)

auth_controller = AuthController(
    service=auth_service,
    redirect_factory=redirect_factory,
    cookie_factory=cookie_factory,
    frontend_url=settings.frontend_url,
    home_url=settings.home_url,
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


@auth_router.get("/refresh")
async def refresh(refresh_token=Depends(get_refresh_token)):
    try:
        return await auth_controller.refresh(refresh_token)
    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")


@auth_router.get("/me")
async def me(current_user=Depends(get_current_user)):
    try:
        user_id = current_user.get("user_id")
        return await auth_controller.me(user_id)
    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")


@auth_router.get("/check")
async def check(current_user=Depends(get_current_user)):
    try:
        return {"status": "ok"}
    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")


@auth_router.post("/logout")
async def logout(refresh_token=Depends(get_refresh_token)):
    try:
        return await auth_controller.logout(refresh_token)
    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")
