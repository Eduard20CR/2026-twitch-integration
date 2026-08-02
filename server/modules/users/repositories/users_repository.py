from sqlmodel import Session, select

from common.db.error_handling import handle_database_errors
from modules.auth.schemas.create_user_dto import CreateUserDTO
from common.db.models.users_model import User


class UsersRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    @handle_database_errors
    async def get_by_id(self, user_id) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await self.db_session.exec(statement)
        return result.first()

    @handle_database_errors
    async def get_by_twitch_id(self, sub: str) -> User | None:
        statement = select(User).where(User.sub == sub)
        result = await self.db_session.exec(statement)
        return result.first()

    @handle_database_errors
    async def create(self, create_user_dto: CreateUserDTO) -> User | None:
        user = User(
            username=create_user_dto.username,
            email=create_user_dto.email,
            sub=create_user_dto.sub,
            provider=create_user_dto.provider,
            profile_image_url=create_user_dto.profile_image_url,
        )

        self.db_session.add(user)
        await self.db_session.flush()
        return user
