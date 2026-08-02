from sqlmodel import Session, select

from common.db.models.oauth_connections_model import OAuthConnection
from modules.auth.exceptions.exceptions import OAuthConnectionCreationError, OAuthConnectionNotFound
from modules.auth.schemas.create_oauth_connection_dto import CreateOAuthConnectionDTO


class OauthConnectionsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, createOAuthConnectionCommand: CreateOAuthConnectionDTO):
        try:
            oauth_connection = OAuthConnection(
                access_token_encrypted=createOAuthConnectionCommand.access_token_encrypted,
                refresh_token_encrypted=createOAuthConnectionCommand.refresh_token_encrypted,
                access_token_expires_at=createOAuthConnectionCommand.access_token_expires_at,
                user_id=createOAuthConnectionCommand.user_id,
            )

            self.db_session.add(oauth_connection)
            await self.db_session.flush()

            return oauth_connection

        except Exception as e:
            print(repr(e))
            raise OAuthConnectionCreationError("Failed to create session") from e

    async def get_by_user_id(self, user_id: int) -> OAuthConnection:
        statement = (
            select(OAuthConnection)
            .where(OAuthConnection.user_id == user_id)
            .order_by(OAuthConnection.access_token_expires_at.desc())
            .limit(1)
        )

        result = await self.db_session.exec(statement)
        connection = result.first()

        if connection is None:
            raise OAuthConnectionNotFound(user_id)

        return connection

    async def update(self, update_oauth_connection_command: CreateOAuthConnectionDTO):
        statement = (
            select(OAuthConnection)
            .where(OAuthConnection.user_id == update_oauth_connection_command.user_id)
            .order_by(OAuthConnection.access_token_expires_at.desc())
            .limit(1)
        )

        result = await self.db_session.exec(statement)
        connection = result.first()

        if connection is None:
            raise OAuthConnectionNotFound(update_oauth_connection_command.user_id)

        connection.access_token_encrypted = update_oauth_connection_command.access_token_encrypted
        connection.refresh_token_encrypted = update_oauth_connection_command.refresh_token_encrypted
        connection.access_token_expires_at = update_oauth_connection_command.access_token_expires_at

        self.db_session.add(connection)
        await self.db_session.flush()

        return connection
