from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class SessionDTO(BaseModel):
    id: UUID
    user_id: UUID
    refresh_token_hash: str
    ip_address: str
    user_agent: str
    expires_at: datetime
    created_at: datetime
