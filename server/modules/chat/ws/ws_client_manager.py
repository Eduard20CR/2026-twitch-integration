from typing import Dict

from modules.chat.ws.ws_client_connection import WsClientConnection
from modules.chat.ws.ws_client_room import WsClientRoom


class WsClientManager:
    def __init__(self):
        self.rooms: Dict[str, WsClientRoom] = {}
        self.twitch_connections: Dict[str, WsClientConnection] = {}

    def get_room(self, room_id: str) -> WsClientRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = WsClientRoom()

        return self.rooms[room_id]

    def add_user_to_room(self, room_id: str, connection: WsClientConnection):
        room = self.get_room(room_id)
        room.add_connection(connection)

    def remove_user_from_room(self, room_id: str, connection_id: str):
        room = self.rooms.get(room_id)

        if room is None:
            return

        room.remove_connection(connection_id)

        if room.is_empty():
            del self.rooms[room_id]


ws_client_manager = WsClientManager()
