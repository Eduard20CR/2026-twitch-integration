import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

from modules.auth.models.users_model import User
from modules.auth.models.user_sessions_model import UserSession
from modules.auth.models.oauth_connections_model import OAuthConnection

load_dotenv()

db_url = os.environ.get(
    "DATABASE_URL_SYNC",
    "postgresql://admin:mysecretpassword@localhost:5432/dev-twitch-integration",
)

engine = create_engine(db_url)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    drop_db_and_tables()
    create_db_and_tables()
