from pydantic import BaseModel


class RefreshTokenDTO(BaseModel):
    raw_refresh_token: str
    refresh_token_hash: str
