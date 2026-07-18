import asyncio
import json

from fastapi import WebSocket

from modules.chat.services.chat_service import ChatService
from modules.chat.ws.ws_client_connection import WsClientConnection


class ChatController:

    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    async def websocket_endpoint(self, websocket: WebSocket, current_user: dict):
        await websocket.accept()

        ws_connection = WsClientConnection(websocket)

        await self.chat_service.websocket_endpoint(ws_connection, current_user)
