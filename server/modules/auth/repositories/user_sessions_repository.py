from sqlmodel import Session, select
from uuid import UUID
from modules.auth.exceptions.domain import SessionCreationError
from common.db.models.user_sessions_model import UserSession
from modules.auth.repositories.oauth_connections_repository import handle_database_errors
from modules.auth.schemas.create_session_dto import CreateSessionDTO


class SessionsRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    @handle_database_errors
    async def get_by_id(self, session_id: UUID):
        statement = select(UserSession).where(UserSession.id == session_id)
        result = await self.db_session.exec(statement)
        return result.first()

    @handle_database_errors
    async def get_by_user_id(self, user_id: UUID):
        statement = select(UserSession).where(UserSession.user_id == user_id)
        result = await self.db_session.exec(statement)
        return result.first()

    @handle_database_errors
    async def get_by_refresh_token(self, refresh_token_hash: str):
        statement = select(UserSession).where(UserSession.refresh_token_hash == refresh_token_hash)
        result = await self.db_session.exec(statement)
        return result.first()

    @handle_database_errors
    async def create(self, create_session_dto: CreateSessionDTO):
        session = UserSession(
            user_id=create_session_dto.user_id,
            refresh_token_hash=create_session_dto.refresh_token_hash,
            ip_address=create_session_dto.ip_address,
            user_agent=create_session_dto.user_agent,
            expires_at=create_session_dto.expires_at,
        )

        self.db_session.add(session)
        await self.db_session.flush()
        return session

    @handle_database_errors
    async def delete_by_refresh_token_hash(self, refresh_token_hash: str):
        statement = select(UserSession).where(UserSession.refresh_token_hash == refresh_token_hash)
        result = await self.db_session.exec(statement)
        session = result.first()

        if session is None:
            return False

        await self.db_session.delete(session)
        return True
