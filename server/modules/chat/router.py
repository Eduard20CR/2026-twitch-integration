import asyncio
import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from common.dependencies.get_current_user_ws import get_current_user_ws
from modules.chat.controller import ChatController
from modules.chat.ws.ws_client_connection import WsClientConnection
from modules.chat.ws.ws_client_manager import ws_client_manager

chatController = ChatController()

chat_router = APIRouter(prefix="/api/chat")


@chat_router.websocket("")
async def websocket_endpoint(websocket: WebSocket, current_user=Depends(get_current_user_ws)):
    await chatController.websocket_endpoint(websocket, current_user)
