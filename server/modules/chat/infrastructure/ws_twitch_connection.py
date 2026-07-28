import asyncio
from common.logging.logger import logger
from modules.chat.infrastructure.ws_twitch_event_sub_connection import WsTwitchEventSubConnection
from modules.chat.infrastructure.ws_twitch_subscription import TwitchSubscription


class WsTwitchConnection:

    def __init__(
        self,
        client_id: str,
        access_token: str,
        user_id: str,
    ):
        self.user_id = user_id

        self.eventsub_connection = WsTwitchEventSubConnection()

        self.subscription = None

        self.client_id = client_id
        self.access_token = access_token

        logger.info(
            {
                "message": "WsTwitchConnection created",
                "user_id": self.user_id,
                "client_id": self.client_id,
                "access_token": self.access_token,
            }
        )

    async def connect(self):

        logger.info(
            {
                "message": "Connecting to Twitch EventSub",
            }
        )

        await self.eventsub_connection.connect()

        # Aquí tenemos que esperar a que Twitch mande session_welcome
        while self.eventsub_connection.get_session_id() is None:
            await asyncio.sleep(0.5)
            logger.info(
                {
                    "message": "Waiting for Twitch EventSub session_id",
                }
            )

        logger.info(
            {
                "message": "Twitch EventSub connected",
                "session_id": self.eventsub_connection.get_session_id(),
            }
        )

        self.subscription = TwitchSubscription(
            client_id=self.client_id,
            access_token=self.access_token,
            user_id=self.user_id,
            session_id=self.eventsub_connection.get_session_id(),
        )

        logger.info(
            {
                "message": "Subscribing to Twitch EventSub",
                "session_id": self.eventsub_connection.get_session_id(),
            }
        )

        await self.subscription.subscribe_chat()

        logger.info(
            {
                "message": "Subscribed to Twitch EventSub",
                "session_id": self.eventsub_connection.get_session_id(),
            }
        )

    async def disconnect(self):

        await self.eventsub_connection.disconnect()
