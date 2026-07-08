import uuid

from fastapi import WebSocket


class WsConnection:
    def __init__(self, websocket: WebSocket):
        self.id = str(uuid.uuid4())
        self.websocket = websocket

    async def send(self, message: str):
        await self.websocket.send_text(message)