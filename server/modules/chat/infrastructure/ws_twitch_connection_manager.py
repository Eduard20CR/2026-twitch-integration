from typing import Dict

from common.env.settings import settings
from modules.chat.infrastructure.ws_twitch_connection import WsTwitchConnection
from modules.chat.ws.ws_client_connection import WsClientConnection


class WsTwitchConnectionManager:

    def __init__(self, client_id: str):
        self.connections: Dict[str, WsTwitchConnection] = {}
        self.client_id = client_id

    async def add_connection(self, connection: WsClientConnection):

        user_id = connection.get_user_info().get("sub")

        if user_id in self.connections:
            return

        ws_twitch_connection = WsTwitchConnection(
            client_id=self.client_id,
            access_token=connection.get_access_token(),
            user_id=user_id,
        )

        self.connections[user_id] = ws_twitch_connection

        await ws_twitch_connection.connect()

    async def remove_connection(self, user_id: str):

        connection = self.connections.get(user_id)

        if not connection:
            return

        await connection.disconnect()

        del self.connections[user_id]

    def get_connection(self, user_id: str):

        return self.connections.get(user_id)


ws_twitch_connection_manager = WsTwitchConnectionManager(client_id=settings.twitch_client_id)
