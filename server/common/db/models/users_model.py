from uuid import uuid4, UUID
from datetime import timezone, datetime

from sqlmodel import Column, DateTime, Field, SQLModel


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    email: str
    sub: str = Field(index=True, unique=True)
    provider: str
    profile_image_url: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
