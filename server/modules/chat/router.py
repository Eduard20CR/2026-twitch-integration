import asyncio
from typing import Dict
import uuid

from fastapi import APIRouter, Depends, FastAPI, WebSocket, WebSocketDisconnect

from common.dependencies.get_current_user_ws import get_current_user_ws

chat_router = APIRouter(prefix="/api/chat")


@chat_router.websocket("")
async def websocket_endpoint(websocket: WebSocket, _=Depends(get_current_user_ws)):
    await websocket.accept()

    connection_id = str(uuid.uuid4())

    receiver = asyncio.create_task(receive_messages(websocket, connection_id))

    ping_sender = asyncio.create_task(send_ping(websocket))

    done, pending = await asyncio.wait([receiver, ping_sender], return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    print("Connection closed")


async def send_ping(websocket: WebSocket):
    while True:
        await asyncio.sleep(3)
        await websocket.send_text("ping keep alive")


async def receive_messages(websocket: WebSocket, connection_id: str):
    try:
        while True:
            message = await websocket.receive_text()
            print(f"{connection_id}: {message}")

    except WebSocketDisconnect:
        print(f"{connection_id} disconnected")


class Room:
    connections: Dict[str, WebSocket]

    def __init__(self):
        self.connections = {}

    def add_connection(self, connection_id: str, websocket: WebSocket):
        self.connections[connection_id] = websocket

    def remove_connection(self, connection_id: str):
        self.connections.pop(connection_id, None)

    def broadcast(self, message: str):
        for websocket in self.connections.values():
            asyncio.create_task(websocket.send_text(message))

    def send_message_to_connection(self, connection_id: str, message: str):
        websocket = self.connections.get(connection_id)
        if websocket is not None:
            asyncio.create_task(websocket.send_text(message))


class RoomManager:
    rooms: Dict[str, Room]

    def __init__(self):
        self.rooms = {}

    def get_room(self, room_id: str) -> Room:
        if room_id not in self.rooms:
            self.rooms[room_id] = Room()
        return self.rooms[room_id]


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
