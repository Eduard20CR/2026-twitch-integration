from typing import Any
from pydantic import BaseModel
from datetime import datetime


class EventMessage(BaseModel):
    event: str
    payload: Any
    timestamp: datetime = datetime.now(datetime.timezone.utc)
