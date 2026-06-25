import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

from modules.auth.models.users_model import User
from modules.auth.models.sessions_model import Session

load_dotenv()

db_url = os.environ.get(
    "DATABASE_URL",
    "postgresql://admin:mysecretpassword@localhost:5432/dev-twitch-integration",
)

engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
