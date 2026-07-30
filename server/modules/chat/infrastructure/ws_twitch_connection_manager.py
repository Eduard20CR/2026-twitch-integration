from typing import Dict

from common.logging.logger import logger
from common.env.settings import settings
from modules.chat.infrastructure.ws_twitch_connection import WsTwitchConnection
from modules.chat.ws.ws_client_connection import WsClientConnection


class WsTwitchConnectionManager:

    def __init__(self, client_id: str):
        self.connections: Dict[str, WsTwitchConnection] = {}
        self.client_id = client_id

    async def add_connection(self, connection: WsClientConnection):

        channel_id = connection.get_channel_id()

        if channel_id in self.connections:
            return

        ws_twitch_connection = WsTwitchConnection(
            client_id=self.client_id,
            access_token=connection.get_access_token(),
            channel_id=channel_id,
        )

        self.connections[channel_id] = ws_twitch_connection

        await ws_twitch_connection.connect()

    async def remove_connection(self, channel_id: str):

        connection = self.connections.get(channel_id)

        if not connection:
            return

        logger.info(f"Removing Twitch WebSocket connection for channel_id: {channel_id}")
        await connection.disconnect()

        del self.connections[channel_id]

    def get_connection(self, user_id: str):

        return self.connections.get(user_id)


ws_twitch_connection_manager = WsTwitchConnectionManager(client_id=settings.twitch_client_id)
