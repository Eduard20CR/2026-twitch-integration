import os

from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

db_url = os.environ.get(
    "DATABASE_URL",
    "postgresql://admin:mysecretpassword@localhost:5432/dev-twitch-integration",
)
# create_async_engine
engine = create_engine(db_url, echo=True)
