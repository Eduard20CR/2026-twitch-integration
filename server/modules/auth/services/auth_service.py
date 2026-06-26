import hashlib

from fastapi import Request

from modules.auth.domain.exceptions import OAuthException, TwitchAuthenticationError, UserCreationError
from modules.auth.infrastructure.twitch_auth_client import TwitchAuthClient
from modules.auth.infrastructure.twitch_api_client import TwitchApiClient
from modules.auth.domain.commands import CreateSessionCommand, CreateUserCommand
from common.db.uow import UnitOfWork
from common.utils.random_code_generator import RandomCodeGenerator


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
        return await self.twitch_auth_client.get_login_redirect(request, self.redirect_url)

    async def handle_callback(self, request: Request):
        try:
            twitch_token = await self.twitch_auth_client.exchange_code_for_token(request)

            twitch_access_token = twitch_token["access_token"]
            twitch_refresh_token = twitch_token["refresh_token"]
            expires_at = twitch_token["expires_at"]
            sub = twitch_token["userinfo"]["sub"]
            username = twitch_token["userinfo"]["preferred_username"]
            provider = twitch_token["userinfo"]["iss"]
            ip_address = request.client.host
            user_agent = request.headers.get("user-agent", "")
            twitch_user_info = await self.twitch_api_client.get_user_email_and_profile_picture(sub, twitch_access_token)

            create_user_command = CreateUserCommand(
                username=username,
                sub=sub,
                provider=provider,
                email=twitch_user_info.email,
                profile_image_url=twitch_user_info.profile_image_url,
            )

            async with UnitOfWork() as uow:
                user_found = await uow.users_repository.get_by_twitch_id(sub)

                if not user_found:
                    user_found = await uow.users_repository.create(create_user_command)

                app_refresh_token = RandomCodeGenerator.generate_random_code(32)
                app_refresh_token_hash = hashlib.sha256(app_refresh_token.encode()).hexdigest()

                create_session_command = CreateSessionCommand(
                    user_id=user_found.id,
                    refresh_token_hash=app_refresh_token_hash,
                    expires_at=expires_at,
                    ip_address=ip_address,
                    user_agent=user_agent,
                )

                print(f"Session command: {create_session_command}")

            return twitch_token

        except TwitchAuthenticationError as e:
            raise OAuthException("Twitch OAuth failed") from e

        except UserCreationError as e:
            raise OAuthException("Failed during user creation") from e
