from sqlmodel import Session

from modules.auth.repositories.users_repository import UsersRepository
from modules.auth.repositories.sessions_repository import SessionsRepository

from .db_engine import engine


class UnitOfWork:

    def __enter__(self):
        self.session = Session(engine)

        self.users_repository = UsersRepository(self.session)
        self.sessions_repository = SessionsRepository(self.session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
