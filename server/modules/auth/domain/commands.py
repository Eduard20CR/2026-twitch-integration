from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class CreateUserCommand(BaseModel):
    username: str
    email: str
    sub: str
    provider: str
    profile_image_url: str


class CreateSessionCommand(BaseModel):
    user_id: UUID
    refresh_token_hash: str
    expires_at: datetime
    ip_address: str
    user_agent: str
