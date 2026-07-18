import os

from fastapi import APIRouter, Depends, WebSocket

from common.dependencies.get_current_user_ws import get_current_user_ws
from modules.auth.services.auth_service import DateDelayGenerator, EncryptionService
from modules.chat.controller import ChatController
from modules.chat.infrastructure.twitch_access_token_updater import TwitchAccessTokenUpdater
from modules.chat.services.chat_service import ChatService
from modules.chat.services.twitch_token_service import TwitchTokenService
from modules.chat.services.ws_service import WsService
from modules.chat.infrastructure.ws_twitch_connection_manager import ws_twitch_connection_manager
from modules.chat.ws.ws_client_manager import ws_client_manager
from modules.chat.events.ws_event_bus import ws_event_bus

twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")
twitch_access_token_url = os.getenv("TWITCH_ACCESS_TOKEN_URL")
encryption_key = os.getenv("ENCRYPTION_KEY")


twitch_access_token_updater = TwitchAccessTokenUpdater(
    client_id=twitch_client_id,
    client_secret=twitch_client_secret,
    twitch_token_url=twitch_access_token_url,
)
date_delay_generator = DateDelayGenerator()
encryption_service = EncryptionService(key=encryption_key)

twitch_token_service = TwitchTokenService(
    encryption_service=encryption_service,
    twitch_access_token_updater=twitch_access_token_updater,
    date_delay_generator=date_delay_generator,
)

wsService = WsService(
    ws_client_manager=ws_client_manager,
    ws_twitch_connection_manager=ws_twitch_connection_manager,
    ws_event_bus=ws_event_bus,
)
chatService = ChatService(
    ws_service=wsService,
    twitch_token_service=twitch_token_service,
)
chatController = ChatController(chat_service=chatService)

chat_router = APIRouter(prefix="/api/chat")


@chat_router.websocket("")
async def websocket_endpoint(websocket: WebSocket, current_user=Depends(get_current_user_ws)):
    await chatController.websocket_endpoint(websocket, current_user)
