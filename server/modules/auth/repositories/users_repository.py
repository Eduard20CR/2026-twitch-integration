from sqlmodel import Session

from modules.auth.domain.commands import CreateUserCommand
from modules.auth.models.users_model import User


class UsersRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, user_id):
        pass

    def get_by_twitch_id(self, twitch_id):
        pass

    def create(self, create_user_command: CreateUserCommand):
        user = User(
            username=create_user_command.username,
            email=create_user_command.email,
            sub=create_user_command.sub,
            provider=create_user_command.provider,
        )
        self.db_session.add(user)
