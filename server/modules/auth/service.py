import os

from fastapi import Request

from common.auth.auth import oauth
from .exceptions import OAuthException


class AuthService:

    async def get_login_redirect(self, request: Request):
        redirect_url = os.getenv("REDIRECT_URL")

        if not redirect_url:
            raise RuntimeError("REDIRECT_URL not configured")

        return await oauth.twitch.authorize_redirect(request, redirect_url)

    async def handle_callback(self, request: Request):
        try:
            token = await oauth.twitch.authorize_access_token(request)
            return token

        except Exception as e:
            # aquí NO HTTP, solo error de dominio
            raise OAuthException("Twitch OAuth failed") from e
