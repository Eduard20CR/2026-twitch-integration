from fastapi import Request

from modules.auth.domain.exceptions import OAuthException, TwitchAuthenticationError
from modules.auth.infrastructure.twitch_auth_client import TwitchAuthClient
from modules.auth.infrastructure.twitch_api_client import TwitchApiClient
from modules.auth.domain.commands import CreateUserCommand
from common.db.uow import UnitOfWork


class AuthService:

    def __init__(
        self,
        twitch_auth_client: TwitchAuthClient,
        twitch_api_client: TwitchApiClient,
        redirect_url: str,
    ):
        self.twitch_auth_client = twitch_auth_client
        self.twitch_api_client = twitch_api_client
        self.redirect_url = redirect_url

    async def get_login_redirect(self, request: Request):
        return await self.twitch_auth_client.get_login_redirect(
            request, self.redirect_url
        )

    async def handle_callback(self, request: Request):
        try:
            token = await self.twitch_auth_client.exchange_code_for_token(request)

            access_token = token["access_token"]
            sub = token["userinfo"]["sub"]
            username = token["userinfo"]["preferred_username"]
            provider = token["userinfo"]["iss"]
            twitch_user_info = (
                await self.twitch_api_client.get_user_email_and_profile_picture(
                    sub, access_token
                )
            )

            create_user_command = CreateUserCommand(
                username=username,
                sub=sub,
                provider=provider,
                email=twitch_user_info.email,
                profile_image_url=twitch_user_info.profile_image_url,
            )
            print(f"Creating user with command: {create_user_command}")

            with UnitOfWork() as uow:

                uow.users_repository.create(create_user_command)

            return token

        except TwitchAuthenticationError as e:
            raise OAuthException("Twitch OAuth failed") from e
