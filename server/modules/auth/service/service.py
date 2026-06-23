from fastapi import Request

from modules.auth.domain.exceptions import OAuthException, TwitchAuthenticationError
from modules.auth.infrastructure.twitch_client import TwitchClient


class AuthService:

    def __init__(self, twitch_client: TwitchClient, redirect_url: str):
        self.twitch_client = twitch_client
        self.redirect_url = redirect_url

    async def get_login_redirect(self, request: Request):
        return await self.twitch_client.get_login_redirect(request, self.redirect_url)

    async def handle_callback(self, request: Request):
        try:
            token = await self.twitch_client.exchange_code_for_token(request)

            # LOGICA DE AUTENTICACION Y CREACION DE USUARIO EN LA BASE DE DATOS

            return token

        except TwitchAuthenticationError as e:
            raise OAuthException("Twitch OAuth failed") from e
