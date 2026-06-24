# infrastructure/twitch_client.py

from fastapi import Request
import httpx

from common.auth.auth import oauth
from modules.auth.domain.exceptions import TwitchAuthenticationError
from modules.auth.domain.twitch_user_information import TwitchUserInformation


class TwitchClient:

    def __init__(self, client_id: str):
        self.client_id = client_id

    async def get_login_redirect(self, request: Request, redirect_url: str):
        return await oauth.twitch.authorize_redirect(
            request,
            redirect_url,
        )

    async def exchange_code_for_token(
        self,
        request: Request,
    ):
        try:
            return await oauth.twitch.authorize_access_token(request)

        except Exception as e:
            raise TwitchAuthenticationError() from e

    async def get_user_email_and_profile_picture(
        self, user_sub: str, access_token: str
    ) -> TwitchUserInformation:

        url = f"https://api.twitch.tv/helix/users?id={user_sub}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-Id": self.client_id,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, headers=headers)

        response.raise_for_status()

        response_data = response.json()

        user_email = response_data["data"][0]["email"]
        user_profile_image_url = response_data["data"][0]["profile_image_url"]

        twitch_user_information = TwitchUserInformation(
            email=user_email, profile_image_url=user_profile_image_url
        )

        return twitch_user_information
