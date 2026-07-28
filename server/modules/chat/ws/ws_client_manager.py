from typing import Dict

from modules.chat.ws.ws_client_connection import WsClientConnection
from modules.chat.ws.ws_client_room import WsClientRoom


class WsClientManager:
    def __init__(self):
        self.rooms: Dict[str, WsClientRoom] = {}

    def get_room_by_id(self, room_id: str) -> WsClientRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = WsClientRoom()

        return self.rooms[room_id]

    def add_user_to_room(self, ws_connection: WsClientConnection):
        room = self.get_room_by_id(ws_connection.get_channel_id())
        room.add_connection(ws_connection)

    def remove_user_from_room(self, ws_connection: WsClientConnection):
        room = self.rooms.get(ws_connection.get_channel_id())

        if room is None:
            return

        room.remove_connection_by_id(ws_connection.get_id())
        if room.is_empty():
            del self.rooms[ws_connection.get_channel_id()]

    def is_room_empty(self, room_id: str) -> bool:
        room = self.rooms.get(room_id)

        if room is None:
            return True

        return room.is_empty()


ws_client_manager = WsClientManager()
