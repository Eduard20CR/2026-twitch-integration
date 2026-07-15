from pydantic import BaseModel


class AuthRefreshResultDTO(BaseModel):
    jwt_access_token: str
    access_expires_in: int
