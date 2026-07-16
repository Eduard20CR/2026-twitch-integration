from sqlmodel import Session, select

from common.db.models.oauth_connections_model import OAuthConnection
from modules.auth.domain.commands import CreateOAuthConnectionCommand
from modules.auth.domain.exceptions import OAuthConnectionCreationError


class OauthConnectionsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, createOAuthConnectionCommand: CreateOAuthConnectionCommand):
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

    async def get_by_user_id(self, user_id: int):
        statement = select(OAuthConnection).where(OAuthConnection.user_id == user_id)
        result = await self.db_session.exec(statement)
        return result.first()
