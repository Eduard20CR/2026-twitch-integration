from dataclasses import dataclass


@dataclass
class AuthRefreshResultDTO:
    jwt_access_token: str
    access_expires_in: int
