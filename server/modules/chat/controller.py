import asyncio
import json

from fastapi import Depends, WebSocket, WebSocketDisconnect

from common.dependencies import get_current_user_ws
from modules.chat.router import ws_client_manager
from modules.chat.service.chat_service import ChatService
from modules.chat.ws.ws_client_connection import WsClientConnection


class ChatController:

    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    async def websocket_endpoint(self, websocket: WebSocket, current_user: dict):
        await websocket.accept()

        ws_connection = WsClientConnection(websocket, current_user.get("user_id"))

        await self.chat_service.websocket_endpoint(ws_connection, current_user)
