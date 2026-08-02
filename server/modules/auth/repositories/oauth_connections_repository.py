from sqlmodel import Session, select

from common.db.error_handling import handle_database_errors
from common.db.models.oauth_connections_model import OAuthConnection
from modules.auth.schemas.create_oauth_connection_dto import CreateOAuthConnectionDTO
from modules.auth.schemas.update_oauth_connection_dto import UpdateOAuthConnectionDTO


class OauthConnectionsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @handle_database_errors
    async def create(self, create_oauth_connection_dto: CreateOAuthConnectionDTO):
        oauth_connection = OAuthConnection(
            access_token_encrypted=create_oauth_connection_dto.access_token_encrypted,
            refresh_token_encrypted=create_oauth_connection_dto.refresh_token_encrypted,
            access_token_expires_at=create_oauth_connection_dto.access_token_expires_at,
            user_id=create_oauth_connection_dto.user_id,
        )

        self.db_session.add(oauth_connection)
        await self.db_session.flush()

        return oauth_connection

    @handle_database_errors
    async def get_by_user_id(self, user_id: int) -> OAuthConnection | None:
        statement = (
            select(OAuthConnection)
            .where(OAuthConnection.user_id == user_id)
            .order_by(OAuthConnection.access_token_expires_at.desc())
            .limit(1)
        )

        result = await self.db_session.exec(statement)
        connection = result.first()

        return connection

    @handle_database_errors
    async def update2(self, oauth_connection: OAuthConnection, update_oauth_connection_dto: UpdateOAuthConnectionDTO):

        oauth_connection.access_token_encrypted = update_oauth_connection_dto.access_token_encrypted
        oauth_connection.refresh_token_encrypted = update_oauth_connection_dto.refresh_token_encrypted
        oauth_connection.access_token_expires_at = update_oauth_connection_dto.access_token_expires_at

        self.db_session.add(oauth_connection)
        await self.db_session.flush()

        return oauth_connection
