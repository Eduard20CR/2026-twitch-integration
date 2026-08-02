from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class CreateOAuthConnectionDTO(BaseModel):
    user_id: UUID
    access_token_encrypted: str
    refresh_token_encrypted: str
    access_token_expires_at: datetime
