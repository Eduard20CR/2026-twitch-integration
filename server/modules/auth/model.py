from uuid import uuid4, UUID

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    email: str
    sub: str
    provider: str


class Session(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    access_token: str
    refresh_token_hash: str
    expires_at: datetime
    is_active: bool = Field(default=True)
