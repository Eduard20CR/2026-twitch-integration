from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class CreateSessionDTO(BaseModel):
    user_id: UUID
    refresh_token_hash: str
    expires_at: datetime
    ip_address: str
    user_agent: str
