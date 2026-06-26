from dataclasses import dataclass


@dataclass
class AuthResultDTO:
    jwt_token: str
    refresh_token: str
    access_expires_in: int
    refresh_expires_in: int
