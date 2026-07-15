from pydantic import BaseModel


class WsMessage(BaseModel):
    event: str
    payload: dict
