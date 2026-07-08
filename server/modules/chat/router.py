import asyncio
import json
from typing import Dict
import uuid

from fastapi import APIRouter, Depends, FastAPI, WebSocket, WebSocketDisconnect

from common.dependencies.get_current_user_ws import get_current_user_ws
from modules.chat.ws.ws_connection import WsConnection
from modules.chat.ws import ws_manager

chat_router = APIRouter(prefix="/api/chat")


@chat_router.websocket("")
async def websocket_endpoint(websocket: WebSocket, current_user=Depends(get_current_user_ws)):
    await websocket.accept()

    ws_connection = WsConnection(websocket)

    receiver = asyncio.create_task(receive_messages(ws_connection, current_user))

    ping_sender = asyncio.create_task(send_ping(ws_connection))

    done, pending = await asyncio.wait([receiver, ping_sender], return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    print("Connection closed")


async def send_ping(ws_connection: WsConnection):
    while True:
        await asyncio.sleep(3)
        await ws_connection.websocket.send_text("ping keep alive")


async def receive_messages(ws_connection: WsConnection, current_user):
    try:
        while True:
            message = await ws_connection.websocket.receive_text()
            json_message = json.loads(message)

            event = json_message.get("event")
            payload = json_message.get("payload")

            print(f"{ws_connection.id}: {message}")

            match event:
                case "connect_to_chat_room":
                    # ws_manager.add_user_to_room("", ws_connection)
                    print(f"{ws_connection.id} connected to chat room")
                    print(f"Current user: {current_user}")

                case _:
                    print(f"Unknown event: {event}")

    except WebSocketDisconnect:
        print(f"{ws_connection.id} disconnected")


# ws_url = os.getenv("TWITCH_WS_URL")

# connection = None


# @chat_router.post("/connect", tags=["chat"])
# async def connect():
#     global connection

#     if connection is None:
#         async with websockets.connect(ws_url) as websocket:

#             while True:
#                 message = await websocket.recv()
#                 print(message)

#     return {"message": connection}


# class ConnectionManager:

#     def __init__(self):
#         # Salas de Angular: { "nombre_canal": {ws_angular1, ws_angular2} }
#         self.rooms: Dict[str, Set[WebSocket]] = {}

#         # Tareas de Twitch activas: { "nombre_canal": asyncio.Task }
#         # Esto nos permite saber si ya hay una conexión viva a Twitch para ese canal
#         self.twitch_tasks: Dict[str, asyncio.Task] = {}

#     async def connect(self, channel: str, access_token: str):
#         """Connects to the Twitch WebSocket in a background task for a specific channel using the provided access token."""
#         try:
#             self.websocket = await websockets.connect(self.url)
#             await self.websocket.send(f"PASS oauth:{access_token}")
#             await self.websocket.send(f"NICK {channel}")
#             await self.websocket.send(f"JOIN #{channel}")

#             while True:
#                 message = await self.websocket.recv()
#                 parsed_message = self.parse_message(message)
#                 print(message)

#         except Exception as e:
#             print(f"Error connecting to WebSocket: {e}")

#     async def disconnect(self, channel: str):
#         pass

#     def add_angular_client_to_channel(self, channel: str, websocket: websockets.WebSocketClientProtocol):
#         if channel not in self.channels:
#             self.channels[channel] = []
#         self.channels[channel].append(websocket)

#     def remove_angular_client_from_channel(self, channel: str, websocket: websockets.WebSocketClientProtocol):
#         if channel in self.channels:
#             self.channels[channel].remove(websocket)
#             if not self.channels[channel]:  # If the list is empty, remove the channel
#                 del self.channels[channel]

#     def parse_message(self, message: str):
#         # Implement your message parsing logic here
#         pass


# class TwitchWebSocket:
#     def __init__(self, url):
#         self.url = url
#         self.websocket = None

#     async def connect(self):
#         try:
#             self.websocket = await websockets.connect(self.url)
#             await self.websocket.send("PASS oauth:6izrlbcjh7yl5xiom8xds134ebdnkb")
#             await self.websocket.send("NICK scarus_")
#             await self.websocket.send("JOIN #scarus_")
#         except Exception as e:
#             print(f"Error connecting to WebSocket: {e}")

#     async def listen(self):
#         while True:
#             message = await self.websocket.recv()
#             parsed_message = self.parse_message(message)
#             print(message)

#     def parse_message(self, message):
#         # Implement your message parsing logic here
#         pass


# async def twitch_listener():
#     twitch_web_socket = TwitchWebSocket(ws_url)
#     await twitch_web_socket.connect()
#     await twitch_web_socket.listen()
