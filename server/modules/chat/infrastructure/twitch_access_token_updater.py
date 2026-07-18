import httpx

from modules.auth.domain.exceptions import TwitchAuthenticationError
from modules.chat.schemas.updated_tokens_dto import UpdatedTokensDTO


class TwitchAccessTokenUpdater:

    def __init__(
        self,
        twitch_token_url: str,
        client_id: str,
        client_secret: str,
    ):
        self.twitch_token_url = twitch_token_url
        self.client_id = client_id
        self.client_secret = client_secret

    async def get_new_access_and_refresh_tokens(self, refresh_token: str) -> UpdatedTokensDTO:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.twitch_token_url,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
            )

        if response.status_code != 200:
            raise TwitchAuthenticationError("Failed to refresh Twitch access token")

        data = response.json()

        return UpdatedTokensDTO(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_in=data["expires_in"],
        )
