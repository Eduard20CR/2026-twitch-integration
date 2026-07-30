import asyncio
from asyncio import Task
import json
import websockets
from common.logging.logger import logger
from websockets.client import ClientConnection


class WsTwitchEventSubConnection:

    URL = "wss://eventsub.wss.twitch.tv/ws"

    def __init__(self, on_session_created=None):
        self.websocket: ClientConnection | None = None
        self.session_id: str = None

        self.running: bool = False
        self.task: Task = None

        self.on_session_created = on_session_created

    async def connect(self):
        if self.running:
            return

        self.running = True
        self.task = asyncio.create_task(self._run())

    async def disconnect(self):

        self.running = False

        if self.websocket:
            await self.websocket.close()

        if self.task:
            self.task.cancel()

            try:
                await self.task
            except asyncio.CancelledError:
                pass

        self.websocket = None
        self.session_id = None
        self.task = None

    async def _run(self):

        while self.running:

            try:
                async with websockets.connect(self.URL) as websocket:

                    self.websocket = websocket

                    await self._listen()

            except asyncio.CancelledError:
                raise

            except Exception as e:
                print(f"Twitch websocket disconnected: {e}")

            finally:
                self.websocket = None
                self.session_id = None

            if self.running:
                await asyncio.sleep(5)

    async def _listen(self):

        async for message in self.websocket:
            try:
                data = json.loads(message)
                await self._handle_message(data)
            except Exception as e:
                print(e)

    async def _handle_message(self, data: dict):

        message_type = data["metadata"]["message_type"]

        if message_type == "session_welcome":

            self.session_id = data["payload"]["session"]["id"]

        if self.on_session_created:
            await self.on_session_created(self.session_id)

        elif message_type == "notification":

            print("Twitch event:", data)

    def get_websocket(self) -> ClientConnection:
        return self.websocket

    def get_session_id(self) -> int:
        return self.session_id

    def is_running(self) -> bool:
        return self.running

    def get_task(self) -> Task:
        return self.task
