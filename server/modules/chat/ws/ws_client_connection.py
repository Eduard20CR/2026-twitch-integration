import uuid

from fastapi import WebSocket


class WsClientConnection:
    def __init__(self, websocket: WebSocket, user_id: str):
        self.id = str(uuid.uuid4())
        self.websocket = websocket
        self.user_id = user_id

    async def send(self, message: str):
        await self.websocket.send_text(message)
