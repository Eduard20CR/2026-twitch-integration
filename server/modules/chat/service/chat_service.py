import asyncio
import json

from fastapi import WebSocketDisconnect

from common.dependencies.get_current_user_ws import get_current_user_ws
from modules.chat.router import Depends
from modules.chat.service.ws_service import WsService
from modules.chat.ws.ws_client_manager import WsClientManager
from modules.chat.ws.ws_client_room import WsClientConnection


class ChatService:
    def __init__(self, ws_service: WsService):
        pass

    async def websocket_endpoint(self, ws_connection: WsClientConnection, current_user: dict):

        receiver = asyncio.create_task(self.receive_messages(ws_connection, current_user))

        ping_sender = asyncio.create_task(self.send_ping(ws_connection))

        done, pending = await asyncio.wait([receiver, ping_sender], return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()

        print("Connection closed")

    async def send_ping(self, ws_connection: WsClientConnection):
        while True:
            await asyncio.sleep(15)
            await ws_connection.websocket.send_text("ping keep alive")

    async def receive_messages(self, ws_connection: WsClientConnection, current_user):
        try:
            while True:
                message = await ws_connection.websocket.receive_text()
                json_message = json.loads(message)

                event = json_message.get("event")
                payload = json_message.get("payload")

                print(f"{ws_connection.id}: {message}")

                match event:
                    case "connect_to_chat_room":
                        self.connect_to_chat_room(ws_connection, payload)

                    case "leave_chat_room":
                        self.leave_chat_room(ws_connection, payload)

                    case "pong":
                        print(f"Received pong from {ws_connection.id}")
                        pass

                    case _:
                        print(f"Unknown event: {event}")

        except WebSocketDisconnect:
            print(f"{ws_connection.id} disconnected")

    def connect_to_chat_room(self, ws_connection: WsClientConnection, payload: dict):
        # Aquí puedes implementar la lógica para conectar al usuario a la sala de chat
        print(f"Connecting {ws_connection.id} to room {payload.get('room_id')}")
        # ws_client_manager.add_user_to_room(ws_connection.user_id, ws_connection)
        pass

    def leave_chat_room(self, ws_connection: WsClientConnection, payload: dict):
        # Aquí puedes implementar la lógica para desconectar al usuario de la sala de chat
        print(f"Disconnecting {ws_connection.id} from room {payload.get('room_id')}")
        # ws_client_manager.remove_user_from_room(ws_connection.user_id, ws_connection)
        pass
