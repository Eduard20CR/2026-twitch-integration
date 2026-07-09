import os

from sqlalchemy.ext.asyncio import create_async_engine

db_url = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:mysecretpassword@localhost:5432/dev-twitch-integration",
)
engine = create_async_engine(db_url, echo=False)
