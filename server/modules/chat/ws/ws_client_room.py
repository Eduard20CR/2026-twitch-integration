from typing import Dict

from modules.chat.ws.ws_client_connection import WsClientConnection


class WsClientRoom:
    def __init__(self):
        self.connections: Dict[str, WsClientConnection] = {}

    def add_connection(self, connection: WsClientConnection):
        self.connections[connection.id] = connection

    def remove_connection(self, connection_id: str):
        self.connections.pop(connection_id, None)

    async def broadcast(self, message: str):
        for connection in self.connections.values():
            await connection.send(message)

    async def send_message_to_connection(self, connection_id: str, message: str):
        connection = self.connections.get(connection_id)

        if connection:
            await connection.send(message)

    def get_connection(self, connection_id: str) -> WsClientConnection | None:
        return self.connections.get(connection_id)

    def is_empty(self) -> bool:
        return len(self.connections) == 0
