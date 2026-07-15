from uuid import uuid4, UUID
from datetime import timezone, datetime
from sqlmodel import Column, DateTime, Field, SQLModel


class OAuthConnection(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    access_token_encrypted: str
    refresh_token_encrypted: str
    access_token_expires_at: datetime
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
