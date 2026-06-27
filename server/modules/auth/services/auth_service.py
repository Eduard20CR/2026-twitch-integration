from datetime import time

from fastapi import Request

from modules.auth.domain.exceptions import OAuthException, TwitchAuthenticationError, UserCreationError
from modules.auth.infrastructure.twitch_auth_client import TwitchAuthClient
from modules.auth.infrastructure.twitch_api_client import TwitchApiClient
from modules.auth.domain.commands import CreateSessionCommand, CreateUserCommand
from common.db.uow import UnitOfWork
from common.utils.refresh_token_handler import RefreshTokenHandler
from common.utils.date_delay_generator import DateDelayGenerator
from common.utils.jwt_token_handler import JWTTokenHandler
from modules.auth.schemas.auth_result_dto import AuthResultDTO


class AuthService:

    def __init__(
        self,
        twitch_auth_client: TwitchAuthClient,
        twitch_api_client: TwitchApiClient,
        refresh_token_handler: RefreshTokenHandler,
        jwt_token_handler: JWTTokenHandler,
        date_delay_generator: DateDelayGenerator,
        redirect_url: str,
    ):
        self.twitch_auth_client = twitch_auth_client
        self.twitch_api_client = twitch_api_client
        self.refresh_token_handler = refresh_token_handler
        self.jwt_token_handler = jwt_token_handler
        self.date_delay_generator = date_delay_generator
        self.redirect_url = redirect_url

    async def get_login_redirect(self, request: Request):
        return await self.twitch_auth_client.get_login_redirect(request, self.redirect_url)

    async def handle_callback(self, request: Request):
        try:
            twitch_token = await self.twitch_auth_client.exchange_code_for_token(request)

            twitch_access_token = twitch_token["access_token"]
            twitch_refresh_token = twitch_token["refresh_token"]
            twitch_expires_at = twitch_token["expires_at"]
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

                app_refresh_token = self.refresh_token_handler.generate_random_code(32)
                app_refresh_token_hash = self.refresh_token_handler.hash_code(app_refresh_token)

                app_refresh_token_expires_at = self.date_delay_generator.get_date_plus_days(30)

                create_session_command = CreateSessionCommand(
                    user_id=user_found.id,
                    refresh_token_hash=app_refresh_token_hash,
                    expires_at=app_refresh_token_expires_at,
                    ip_address=ip_address,
                    user_agent=user_agent,
                )

                app_session = await uow.sessions_repository.create(create_session_command)

                current_time = self.date_delay_generator.get_current_utc_time()
                app_jwt_token_expires_at = self.date_delay_generator.get_date_plus_hours(1)
                jwt_token_payload = {
                    "session_id": str(app_session.id),
                    "user_id": str(user_found.id),
                    "iat": int(current_time.timestamp()),
                    "exp": int(app_jwt_token_expires_at.timestamp()),
                    "type": "access",
                }

                client_jwt_token = self.jwt_token_handler.generate_token(payload=jwt_token_payload)

                auth_result_dto = AuthResultDTO(
                    jwt_token=client_jwt_token,
                    refresh_token=app_refresh_token,
                    access_expires_in=int(app_jwt_token_expires_at.timestamp() - current_time.timestamp()),
                    refresh_expires_in=int(app_refresh_token_expires_at.timestamp() - current_time.timestamp()),
                )

            return auth_result_dto

        except TwitchAuthenticationError as e:
            raise OAuthException("Twitch OAuth failed") from e

        except UserCreationError as e:
            raise OAuthException("Failed during user creation") from e

        except Exception as e:
            raise OAuthException("An unexpected error occurred during authentication") from e
