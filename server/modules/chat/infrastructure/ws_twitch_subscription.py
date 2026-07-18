import httpx


class TwitchSubscription:

    EVENTSUB_URL = "https://api.twitch.tv/helix/eventsub/subscriptions"

    def __init__(self, client_id: str, access_token: str, user_id: str, session_id: str):
        self.client_id = client_id
        self.access_token = access_token
        self.user_id = user_id
        self.session_id = session_id

    async def subscribe_chat(self):

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "type": "channel.chat.message",
            "version": "1",
            "condition": {
                "broadcaster_user_id": self.user_id,
                "user_id": self.user_id,
            },
            "transport": {
                "method": "websocket",
                "session_id": self.session_id,
            },
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(self.EVENTSUB_URL, headers=headers, json=payload)

            response.raise_for_status()

            return response.json()
