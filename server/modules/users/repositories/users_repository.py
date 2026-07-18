from sqlmodel import Session, select

from modules.auth.domain.commands import CreateUserCommand
from common.db.models.users_model import User
from modules.auth.domain.exceptions import UserCreationError


class UsersRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_by_id(self, user_id) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await self.db_session.exec(statement)
        return result.first()

    async def get_by_twitch_id(self, sub: str) -> User | None:
        statement = select(User).where(User.sub == sub)
        result = await self.db_session.exec(statement)
        return result.first()

    async def create(self, create_user_command: CreateUserCommand) -> User | None:
        try:

            user = User(
                username=create_user_command.username,
                email=create_user_command.email,
                sub=create_user_command.sub,
                provider=create_user_command.provider,
                profile_image_url=create_user_command.profile_image_url,
            )

            self.db_session.add(user)
            await self.db_session.flush()
            return user

        except Exception as e:
            print(repr(e))
            raise UserCreationError("Failed to create user") from e
