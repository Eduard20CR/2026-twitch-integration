import asyncio
import json
from fastapi import WebSocketDisconnect

from common.logging.logger import logger
from modules.auth.services.auth_service import UnitOfWork
from modules.chat.domain.exceptions import UserNotFoundInDB
from modules.chat.services.twitch_token_service import TwitchTokenService
from modules.chat.services.ws_service import WsService
from modules.chat.ws.ws_client_room import WsClientConnection
from modules.chat.ws.ws_protocol import WsProtocol


class ChatService:
    def __init__(
        self,
        ws_service: WsService,
        twitch_token_service: TwitchTokenService,
    ):
        self.ws_service = ws_service
        self.twitch_token_service = twitch_token_service

    async def websocket_endpoint(self, ws_connection: WsClientConnection, current_user: dict):

        user_id = current_user.get("user_id")
        user_info = await self._get_user_info(user_id)

        if user_info is None:
            await ws_connection.get_websocket().close(code=1008)
            raise UserNotFoundInDB("User not found")
        ws_connection.set_user_info(user_info)

        access_token = await self.twitch_token_service.get_access_token(user_id)
        ws_connection.set_access_token(access_token)
        logger.info(f"User {user_info.get('username')} connected to WebSocket with access token: {access_token}")

        receiver = asyncio.create_task(self._receive_messages(ws_connection))
        ping_sender = asyncio.create_task(self._send_ping(ws_connection))

        done, pending = await asyncio.wait([receiver, ping_sender], return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()

        logger.info(f"WebSocket connection closed for user: {user_info.get('username')}")

    async def _send_ping(self, ws_connection: WsClientConnection):
        while True:
            await asyncio.sleep(30)
            message = WsProtocol.ping().model_dump_json()
            await ws_connection.get_websocket().send_text(message)

    async def _receive_messages(self, ws_connection: WsClientConnection):
        try:
            while True:
                message = await ws_connection.get_websocket().receive_text()
                json_message = json.loads(message)
                event = json_message.get("event")
                payload = json_message.get("payload")

                logger.info({"event": event, "payload": payload})

                match event:
                    case "connect_to_chat_room":
                        await self._on_connect_to_chat_room(ws_connection, payload)
                        await ws_connection.send(WsProtocol.info_message("Connected to chat room").model_dump_json())
                    case "leave_chat_room":
                        self._on_leave_chat_room(ws_connection, payload)
                        await ws_connection.send(WsProtocol.info_message("Left chat room").model_dump_json())
                    case "pong":
                        logger.info("Received pong from client")
                    case _:
                        logger.warning(f"Unknown event received: {event}")

        except WebSocketDisconnect as e:
            logger.info(f"WebSocket disconnected: {e}")

        except Exception as e:
            logger.error(f"Error in WebSocket connection: {e}")

        finally:
            self.ws_service.disconnect_user(websocket=ws_connection)

    # MESSAGE HANDLERS

    async def _on_connect_to_chat_room(self, ws_connection: WsClientConnection, _: dict):
        await self.ws_service.connect_user(websocket=ws_connection)

    def _on_leave_chat_room(self, ws_connection: WsClientConnection, _: dict):
        self.ws_service.disconnect_user(websocket=ws_connection)

    # HELPERS

    async def _get_user_info(self, user_id: str):
        async with UnitOfWork() as uow:
            user_info = await uow.users_repository.get_by_id(user_id)
            if user_info:
                return user_info.model_dump()
            return None
