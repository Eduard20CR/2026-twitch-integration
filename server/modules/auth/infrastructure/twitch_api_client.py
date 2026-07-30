# infrastructure/twitch_client.py

import httpx

from modules.auth.schemas.twitch_user_information_response import TwitchUserInformationResponse


class TwitchApiClient:

    def __init__(self, client_id: str):
        self.client_id = client_id

    async def get_user_email_and_profile_picture(
        self, user_sub: str, access_token: str
    ) -> TwitchUserInformationResponse:

        url = f"https://api.twitch.tv/helix/users?id={user_sub}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-Id": self.client_id,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, headers=headers)

        response.raise_for_status()

        response_data = response.json()
        user_data = response_data["data"][0]

        return TwitchUserInformationResponse(email=user_data["email"], profile_image_url=user_data["profile_image_url"])
