from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from common.dependencies.get_current_user_ws import get_current_user_ws
from modules.chat.controller import ChatController
from modules.chat.services.chat_service import ChatService
from modules.chat.services.ws_service import WsService
from modules.chat.infrastructure.ws_twitch_connection_manager import ws_twitch_connection_manager
from modules.chat.ws.ws_client_manager import ws_client_manager
from modules.chat.events.ws_event_bus import ws_event_bus

wsService = WsService(
    ws_client_manager=ws_client_manager,
    ws_twitch_connection_manager=ws_twitch_connection_manager,
    ws_event_bus=ws_event_bus,
)
chatService = ChatService(ws_service=wsService)
chatController = ChatController(chat_service=chatService)

chat_router = APIRouter(prefix="/api/chat")


@chat_router.websocket("")
async def websocket_endpoint(websocket: WebSocket, current_user=Depends(get_current_user_ws)):
    await chatController.websocket_endpoint(websocket, current_user)
