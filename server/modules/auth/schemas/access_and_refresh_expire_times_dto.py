from pydantic import BaseModel
from datetime import datetime


class AccessAndRefreshExpireTimesDTO(BaseModel):
    access_expires_at: datetime
    refresh_expires_at: datetime
    access_expires_in: int
    refresh_expires_in: int
