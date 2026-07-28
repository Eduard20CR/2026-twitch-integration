from modules.chat.infrastructure.ws_twitch_connection_manager import WsTwitchConnectionManager
from modules.chat.ws.ws_client_connection import WsClientConnection
from modules.chat.ws.ws_client_manager import WsClientManager
from modules.chat.events.ws_event_bus import WsEventBus


class WsService:
    def __init__(
        self,
        ws_client_manager: WsClientManager,
        ws_twitch_connection_manager: WsTwitchConnectionManager,
        ws_event_bus: WsEventBus,
    ):
        self.ws_client_manager = ws_client_manager
        self.ws_twitch_connection_manager = ws_twitch_connection_manager
        self.ws_event_bus = ws_event_bus

    async def connect_user(self, websocket: WsClientConnection):
        channel_username = websocket.get_user_info().get("username")
        access_token = websocket.get_access_token()
        print(f"User connected: {channel_username} with access token: {access_token}")

        self.ws_client_manager.add_user_to_room(websocket)
        await self.ws_twitch_connection_manager.add_connection(websocket)

    def disconnect_user(self, websocket: WsClientConnection):
        self.ws_client_manager.remove_user_from_room(websocket)
