import uuid

from fastapi import WebSocket


class WsClientConnection:
    """Represents a WebSocket connection for a client."""

    def __init__(self, websocket: WebSocket):
        self._id = str(uuid.uuid4())
        self._websocket = websocket
        self._user_info = None

    async def send(self, message: str):
        await self._websocket.send_text(message)

    def get_websocket(self) -> WebSocket:
        return self._websocket

    def get_id(self) -> str:
        return self._id

    def get_user_info(self) -> dict:
        return self.user_info.copy()

    def get_channel_id(self):
        if self.user_info:
            return self.user_info.get("sub")
        return None

    def set_user_info(self, user_info: dict):
        self.user_info = user_info
