from fastapi import Request

from modules.auth.domain.exceptions import OAuthException, TwitchAuthenticationError
from modules.auth.infrastructure.twitch_client import TwitchClient
from modules.auth.domain.commands import CreateUserCommand
from common.db.uow import UnitOfWork


class AuthService:

    def __init__(self, twitch_client: TwitchClient, redirect_url: str):
        self.twitch_client = twitch_client
        self.redirect_url = redirect_url

    async def get_login_redirect(self, request: Request):
        return await self.twitch_client.get_login_redirect(request, self.redirect_url)

    async def handle_callback(self, request: Request):
        try:
            token = await self.twitch_client.exchange_code_for_token(request)

            access_token = token["access_token"]
            sub = token["userinfo"]["sub"]
            username = token["userinfo"]["preferred_username"]
            provider = token["userinfo"]["iss"]
            twitch_user_info = (
                await self.twitch_client.get_user_email_and_profile_picture(
                    sub, access_token
                )
            )

            # with UnitOfWork() as uow:
            # create_user_command = CreateUserCommand(
            # username=token["userinfo"]["preferred_username"],
            # email=token["userinfo"]["email"],
            # sub=token["userinfo"]["sub"],
            # provider=token["userinfo"]["iss"],
            # )
            # pass

            return token

        except TwitchAuthenticationError as e:
            raise OAuthException("Twitch OAuth failed") from e
