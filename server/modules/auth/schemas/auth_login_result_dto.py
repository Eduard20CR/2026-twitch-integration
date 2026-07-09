from dataclasses import dataclass


@dataclass
class AuthLoginResultDTO:
    jwt_access_token: str
    jwt_refresh_token: str
    access_expires_in: int
    refresh_expires_in: int
