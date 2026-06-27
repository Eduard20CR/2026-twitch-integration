from sqlmodel import Session, select
from uuid import UUID
from modules.auth.domain.commands import CreateSessionCommand
from modules.auth.domain.exceptions import SessionCreationError
from modules.auth.models.user_sessions_model import UserSession


class SessionsRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_by_id(self, session_id: UUID):
        statement = select(UserSession).where(UserSession.id == session_id)
        result = await self.db_session.exec(statement)
        return result.first()

    async def get_by_user_id(self, user_id: UUID):
        statement = select(UserSession).where(UserSession.user_id == user_id)
        result = await self.db_session.exec(statement)
        return result.first()

    async def create(self, create_session_command: CreateSessionCommand):
        try:
            session = UserSession(
                user_id=create_session_command.user_id,
                refresh_password_hash=create_session_command.refresh_password_hash,
                ip_address=create_session_command.ip_address,
                user_agent=create_session_command.user_agent,
                expires_at=create_session_command.expires_at,
            )

            self.db_session.add(session)
            await self.db_session.flush()
            return session

        except Exception as e:
            print(repr(e))
            raise SessionCreationError("Failed to create session") from e
