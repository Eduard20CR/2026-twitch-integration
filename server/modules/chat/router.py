import asyncio
import os
from typing import Dict, Set

from fastapi import APIRouter, FastAPI, WebSocket
import websockets

chat_router = APIRouter()

ws_url = os.getenv("TWITCH_WS_URL")

connection = None


@chat_router.post("/connect", tags=["chat"])
async def connect():
    global connection

    if connection is None:
        async with websockets.connect(ws_url) as websocket:

            while True:
                message = await websocket.recv()
                print(message)

    return {"message": connection}


class ConnectionManager:

    def __init__(self):
        # Salas de Angular: { "nombre_canal": {ws_angular1, ws_angular2} }
        self.rooms: Dict[str, Set[WebSocket]] = {}

        # Tareas de Twitch activas: { "nombre_canal": asyncio.Task }
        # Esto nos permite saber si ya hay una conexión viva a Twitch para ese canal
        self.twitch_tasks: Dict[str, asyncio.Task] = {}

    async def connect(self, channel: str, access_token: str):
        """Connects to the Twitch WebSocket in a background task for a specific channel using the provided access token."""
        try:
            self.websocket = await websockets.connect(self.url)
            await self.websocket.send(f"PASS oauth:{access_token}")
            await self.websocket.send(f"NICK {channel}")
            await self.websocket.send(f"JOIN #{channel}")

            while True:
                message = await self.websocket.recv()
                parsed_message = self.parse_message(message)
                print(message)

        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")

    async def disconnect(self, channel: str):
        pass

    def add_angular_client_to_channel(self, channel: str, websocket: websockets.WebSocketClientProtocol):
        if channel not in self.channels:
            self.channels[channel] = []
        self.channels[channel].append(websocket)

    def remove_angular_client_from_channel(self, channel: str, websocket: websockets.WebSocketClientProtocol):
        if channel in self.channels:
            self.channels[channel].remove(websocket)
            if not self.channels[channel]:  # If the list is empty, remove the channel
                del self.channels[channel]

    def parse_message(self, message: str):
        # Implement your message parsing logic here
        pass


class TwitchWebSocket:
    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.url)
            await self.websocket.send("PASS oauth:6izrlbcjh7yl5xiom8xds134ebdnkb")
            await self.websocket.send("NICK scarus_")
            await self.websocket.send("JOIN #scarus_")
        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")

    async def listen(self):
        while True:
            message = await self.websocket.recv()
            parsed_message = self.parse_message(message)
            print(message)

    def parse_message(self, message):
        # Implement your message parsing logic here
        pass


async def twitch_listener():
    twitch_web_socket = TwitchWebSocket(ws_url)
    await twitch_web_socket.connect()
    await twitch_web_socket.listen()
