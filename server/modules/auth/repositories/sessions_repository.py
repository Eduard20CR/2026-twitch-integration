from sqlmodel import Session


class SessionsRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, session_id):
        pass

    def create(self, session):
        pass
