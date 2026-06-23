# infrastructure/twitch_client.py

from fastapi import Request

from common.auth.auth import oauth
from modules.auth.domain.exceptions import TwitchAuthenticationError


class TwitchClient:

    async def get_login_redirect(
        self,
        request: Request,
        redirect_url: str,
    ):
        return await oauth.twitch.authorize_redirect(
            request,
            redirect_url,
        )

    async def exchange_code_for_token(
        self,
        request: Request,
    ):
        try:
            return await oauth.twitch.authorize_access_token(request)

        except Exception as e:
            raise TwitchAuthenticationError() from e
