from fastapi import Request

from modules.auth.domain.exceptions import OAuthException, TwitchAuthenticationError, UserCreationError
from modules.auth.infrastructure.twitch_auth_client import TwitchAuthClient
from modules.auth.infrastructure.twitch_api_client import TwitchApiClient
from modules.auth.domain.commands import CreateSessionCommand, CreateUserCommand
from common.db.uow import UnitOfWork
from common.tokens.refresh_token_handler import RefreshTokenHandler
from common.dates.date_delay_generator import DateDelayGenerator
from common.tokens.jwt_token_handler import JWTTokenHandler
from modules.auth.schemas.auth_login_result_dto import AuthLoginResultDTO
from modules.auth.schemas.user_dto import UserDTO
from modules.auth.schemas.session_dto import SessionDTO
from modules.auth.schemas.auth_refresh_result_dto import AuthRefreshResultDTO
from modules.auth.schemas.user_me_info_dto import UserMeInfoDTO


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
            twitch_token = await self._get_twitch_token(request)

            print(f"Twitch token received: {twitch_token}")

            user = await self._get_or_create_user(twitch_token, request)

            session, raw_refresh_token = await self._create_session(user, request)

            access_token, access_exp, refresh_exp = self._create_token_and_expire_time(user.id, session.id)

            return self._build_auth_login_response(access_token, raw_refresh_token, access_exp, refresh_exp)

        except TwitchAuthenticationError as e:
            print(repr(e))
            raise OAuthException("Twitch OAuth failed") from e

        except UserCreationError as e:
            print(repr(e))
            raise OAuthException("Failed during user creation") from e

        except Exception as e:
            print(repr(e))
            raise OAuthException("An unexpected error occurred during authentication") from e

    async def refresh_tokens(self, refresh_token: str):
        try:
            async with UnitOfWork() as uow:
                refresh_token_hashed = self.refresh_token_handler.hash_code(refresh_token)
                session = await uow.sessions_repository.get_by_refresh_token(refresh_token_hashed)

                if not session:
                    raise OAuthException("Invalid refresh token")

                if session.expires_at < self.date_delay_generator.get_current_utc_time():
                    raise OAuthException("Refresh token has expired")

                access_token, access_exp, _ = self._create_token_and_expire_time(session.user_id, session.id)

                return self._build_auth_refresh_response(access_token, access_exp)

        except Exception as e:
            print(repr(e))
            raise OAuthException("Failed to refresh tokens") from e

    async def get_current_user(self, user_id: str):
        try:
            async with UnitOfWork() as uow:
                user = await uow.users_repository.get_by_id(user_id)

                if not user:
                    raise OAuthException("User not found")

                return UserMeInfoDTO(username=user.username, email=user.email, profile_image_url=user.profile_image_url)

        except Exception as e:
            print(repr(e))
            raise OAuthException("Failed to retrieve current user") from e

    async def logout(self, refresh_token: str):
        try:
            async with UnitOfWork() as uow:
                refresh_token_hashed = self.refresh_token_handler.hash_code(refresh_token)
                session = await uow.sessions_repository.get_by_refresh_token(refresh_token_hashed)

                if not session:
                    raise OAuthException("Invalid refresh token")

                await uow.sessions_repository.delete_by_refresh_token_hash(refresh_token_hashed)
        except Exception as e:
            print(repr(e))
            raise OAuthException("Failed to logout") from e

    async def _get_twitch_token(self, request: Request):
        return await self.twitch_auth_client.exchange_code_for_token(request)

    async def _get_or_create_user(self, twitch_token, request: Request):
        sub = twitch_token["userinfo"]["sub"]
        username = twitch_token["userinfo"]["preferred_username"]
        provider = twitch_token["userinfo"]["iss"]
        access_token = twitch_token["access_token"]

        twitch_user_info = await self.twitch_api_client.get_user_email_and_profile_picture(sub, access_token)

        async with UnitOfWork() as uow:
            user = await uow.users_repository.get_by_twitch_id(sub)

            if user:
                return UserDTO(id=user.id, username=user.username, sub=user.sub)

            create_user_command = CreateUserCommand(
                username=username,
                sub=sub,
                provider=provider,
                email=twitch_user_info.email,
                profile_image_url=twitch_user_info.profile_image_url,
            )

            user = await uow.users_repository.create(create_user_command)

            return UserDTO(id=user.id, username=user.username, sub=user.sub)

    async def _create_session(self, user, request: Request):
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent", "")

        raw_refresh_token = self.refresh_token_handler.generate_random_code(32)
        refresh_token_hash = self.refresh_token_handler.hash_code(raw_refresh_token)
        refresh_token_expires_at = self.date_delay_generator.get_date_plus_days(30)

        async with UnitOfWork() as uow:

            create_session_command = CreateSessionCommand(
                user_id=user.id,
                refresh_token_hash=refresh_token_hash,
                expires_at=refresh_token_expires_at,
                ip_address=ip_address,
                user_agent=user_agent,
            )

            session = await uow.sessions_repository.create(create_session_command)

            session_dto = SessionDTO(
                id=session.id,
                user_id=session.user_id,
                refresh_token_hash=session.refresh_token_hash,
                ip_address=session.ip_address,
                user_agent=session.user_agent,
                expires_at=session.expires_at,
                created_at=session.created_at,
            )

        return session_dto, raw_refresh_token

    def _create_access_token(self, user_id, session_id, expires_at):
        now = self.date_delay_generator.get_current_utc_time()

        payload = {
            "session_id": str(session_id),
            "user_id": str(user_id),
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
            "type": "access",
        }

        return self.jwt_token_handler.generate_token(payload)

    def _create_token_and_expire_time(self, user_id, session_id):
        access_expires_at = self.date_delay_generator.get_date_plus_hours(2)
        refresh_expires_at = self.date_delay_generator.get_date_plus_days(30)

        access_token = self._create_access_token(
            user_id=user_id,
            session_id=session_id,
            expires_at=access_expires_at,
        )

        access_expires_in = int((access_expires_at - self.date_delay_generator.get_current_utc_time()).total_seconds())
        refresh_expires_in = int(
            (refresh_expires_at - self.date_delay_generator.get_current_utc_time()).total_seconds()
        )

        return access_token, access_expires_in, refresh_expires_in

    def _build_auth_login_response(self, access_token, refresh_token, access_expires_in, refresh_expires_in):
        return AuthLoginResultDTO(
            jwt_access_token=access_token,
            jwt_refresh_token=refresh_token,
            access_expires_in=access_expires_in,
            refresh_expires_in=refresh_expires_in,
        )

    def _build_auth_refresh_response(self, access_token, access_expires_in):
        return AuthRefreshResultDTO(
            jwt_access_token=access_token,
            access_expires_in=access_expires_in,
        )
