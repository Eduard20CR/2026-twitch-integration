import asyncio
from asyncio import Task
import json
import websockets
from websockets.client import ClientConnection


class WsTwitchEventSubConnection:

    URL = "wss://eventsub.wss.twitch.tv/ws"

    def __init__(self):
        self.connection: ClientConnection = None
        self.session_id: int = None

        self.running: bool = False
        self.task: Task = None

    async def connect(self):
        self.running = True
        self.task = asyncio.create_task(self._run())

    async def disconnect(self):

        self.running = False

        if self.websocket:
            await self.websocket.close()

        if self.task:
            self.task.cancel()

    async def _run(self):

        async with websockets.connect(self.URL) as websocket:

            self.websocket = websocket

            await self._listen()

    async def _listen(self):

        async for message in self.websocket:

            data = json.loads(message)

            await self._handle_message(data)

    async def _handle_message(self, data: dict):

        message_type = data["metadata"]["message_type"]

        if message_type == "session_welcome":

            self.session_id = data["payload"]["session"]["id"]

            print("Connected Twitch session:", self.session_id)

        elif message_type == "notification":

            print("Twitch event:", data)

    def get_websocket(self) -> ClientConnection:
        return self.connection

    def get_session_id(self) -> int:
        return self.session_id

    def is_running(self) -> bool:
        return self.running

    def get_task(self) -> Task:
        return self.task
