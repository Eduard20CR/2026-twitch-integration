from pydantic import BaseModel


class AuthLoginResultDTO(BaseModel):
    jwt_access_token: str
    jwt_refresh_token: str
    access_expires_in: int
    refresh_expires_in: int
