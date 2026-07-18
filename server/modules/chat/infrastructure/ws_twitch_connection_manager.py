from typing import Dict

from modules.chat.infrastructure.ws_twitch_connection import WsTwitchConnection


class WsTwitchConnectionManager:

    def __init__(self):
        self.connections: Dict[str, WsTwitchConnection] = {}

    async def add_connection(self, connection: WsTwitchConnection):

        user_id = connection.user_id

        if user_id in self.connections:
            return

        self.connections[user_id] = connection

        await connection.connect()

    async def remove_connection(self, user_id: str):

        connection = self.connections.get(user_id)

        if not connection:
            return

        await connection.disconnect()

        del self.connections[user_id]

    def get_connection(self, user_id: str):

        return self.connections.get(user_id)
