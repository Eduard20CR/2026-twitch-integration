from sqlmodel.ext.asyncio.session import AsyncSession

from modules.auth.repositories.oauth_connections_repository import OauthConnectionsRepository
from modules.users.repositories.users_repository import UsersRepository
from modules.auth.repositories.user_sessions_repository import SessionsRepository

from .db_engine import engine


class UnitOfWork:

    async def __aenter__(self):
        self.session = AsyncSession(engine)

        self.users_repository = UsersRepository(self.session)
        self.sessions_repository = SessionsRepository(self.session)
        self.oauth_connections_repository = OauthConnectionsRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
