from time import timezone
from uuid import uuid4, UUID

from datetime import datetime

from sqlmodel import DateTime, Field, SQLModel


class Session(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    refresh_token_hash: str
    ip_address: str
    user_agent: str
    expires_at: datetime
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )
