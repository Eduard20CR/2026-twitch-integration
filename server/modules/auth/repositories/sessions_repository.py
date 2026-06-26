from sqlmodel import Session
from uuid import UUID
from modules.auth.domain.commands import CreateSessionCommand


class SessionsRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, session_id: UUID):
        pass

    def get_by_user_id(self, user_id: UUID):
        pass

    def create(self, create_session_command: CreateSessionCommand):
        pass
