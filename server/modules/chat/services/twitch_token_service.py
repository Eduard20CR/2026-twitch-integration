from datetime import datetime
from datetime import datetime, timezone

from common.dates.date_delay_generator import DateDelayGenerator
from common.db.uow import UnitOfWork
from common.security.encryption import EncryptionService
from modules.auth.exceptions.domain import OAuthConnectionNotFound
from modules.auth.repositories.oauth_connections_repository import OAuthConnection, UpdateOAuthConnectionDTO
from modules.chat.infrastructure.twitch_access_token_updater import TwitchAccessTokenUpdater


class TwitchTokenService:

    def __init__(
        self,
        encryption_service: EncryptionService,
        twitch_access_token_updater: TwitchAccessTokenUpdater,
        date_delay_generator: DateDelayGenerator,
    ):
        self.encryption_service = encryption_service
        self.twitch_access_token_updater = twitch_access_token_updater
        self.date_delay_generator = date_delay_generator

    async def get_access_token(self, user_id: str) -> str:
        async with UnitOfWork() as uow:

            oauth_connection = await uow.oauth_connections_repository.get_by_user_id(user_id)

            if oauth_connection is None:
                raise Exception("OAuth connection not found")

            if not self._is_expired(oauth_connection.access_token_expires_at):
                return self.encryption_service.decrypt(oauth_connection.access_token_encrypted)

            return await self._refresh_access_token(uow, oauth_connection)

    async def _refresh_access_token(self, uow: UnitOfWork, oauth_connection: OAuthConnection) -> str:

        refresh_token = self.encryption_service.decrypt(oauth_connection.refresh_token_encrypted)

        tokens = await self.twitch_access_token_updater.get_new_access_and_refresh_tokens(refresh_token)

        update_oauth_connection_dto = UpdateOAuthConnectionDTO(
            user_id=oauth_connection.user_id,
            access_token_encrypted=self.encryption_service.encrypt(tokens.access_token),
            refresh_token_encrypted=self.encryption_service.encrypt(tokens.refresh_token),
            access_token_expires_at=(self.date_delay_generator.get_date_plus_seconds(tokens.expires_in)),
        )

        oauth_connection = await uow.oauth_connections_repository.get_by_user_id(oauth_connection.user_id)

        if oauth_connection is None:
            raise OAuthConnectionNotFound(oauth_connection.user_id)

        await uow.oauth_connections_repository.update(oauth_connection, update_oauth_connection_dto)

        return tokens.access_token

    def _is_expired(self, expiration: datetime) -> bool:
        now = self.date_delay_generator.get_current_utc_time()

        if expiration.tzinfo is None:
            expiration = expiration.replace(tzinfo=timezone.utc)

        return now >= expiration
