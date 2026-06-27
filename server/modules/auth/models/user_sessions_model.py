from uuid import uuid4, UUID
from datetime import timezone, datetime, timedelta
from sqlmodel import Column, DateTime, Field, SQLModel


class UserSession(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    refresh_password_hash: str
    ip_address: str
    user_agent: str
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
