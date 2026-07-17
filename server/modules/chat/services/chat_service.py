import asyncio
import json
from common.logging.logging import logger
from datetime import datetime, timezone

from fastapi import WebSocketDisconnect

from modules.auth.domain.commands import UpdateOAuthConnectionCommand
from modules.auth.services.auth_service import DateDelayGenerator, EncryptionService, UnitOfWork
from modules.chat.domain.exceptions import UserNotFoundInDB
from modules.chat.infrastructure.twitch_access_token_updater import TwitchAccessTokenUpdater
from modules.chat.services.ws_service import WsService
from modules.chat.ws.ws_client_room import WsClientConnection
from modules.chat.ws.ws_protocol import WsProtocol


class ChatService:
    def __init__(
        self,
        ws_service: WsService,
        date_delay_generator: DateDelayGenerator,
        encryption_service: EncryptionService,
        twitch_access_token_updater: TwitchAccessTokenUpdater,
    ):
        self.ws_service = ws_service
        self.date_delay_generator = date_delay_generator
        self.encryption_service = encryption_service
        self.twitch_access_token_updater = twitch_access_token_updater

    async def websocket_endpoint(self, ws_connection: WsClientConnection, current_user: dict):

        user_id = current_user.get("user_id")
        user_info = await self._get_user_info(user_id)

        if user_info is None:
            await ws_connection.get_websocket().close(code=1008)
            raise UserNotFoundInDB("User not found")
        ws_connection.set_user_info(user_info)

        user_access_token = await self._get_access_token(user_id)
        logger.info(f"User {user_info.get('username')} connected to WebSocket with access token: {user_access_token}")

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
                        self._on_connect_to_chat_room(ws_connection, payload)
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

    def _on_connect_to_chat_room(self, ws_connection: WsClientConnection, _: dict):
        self.ws_service.connect_user(websocket=ws_connection)

    def _on_leave_chat_room(self, ws_connection: WsClientConnection, _: dict):
        self.ws_service.disconnect_user(websocket=ws_connection)

    # HELPERS

    async def _get_user_info(self, user_id: str):
        async with UnitOfWork() as uow:
            user_info = await uow.users_repository.get_by_id(user_id)
            if user_info:
                return user_info.model_dump()
            return None

    async def _get_access_token(self, user_id: str):
        async with UnitOfWork() as uow:
            oauth_info = await uow.oauth_connections_repository.get_by_user_id(user_id)

            current_time = self.date_delay_generator.get_current_utc_time()
            token_expiration_at = oauth_info.access_token_expires_at

            is_token_expired = self.is_token_expired(token_expiration_at, current_time)

            if not is_token_expired:
                encrypted_access_token = oauth_info.access_token_encrypted
                unencrypted_access_token = self.encryption_service.decrypt(encrypted_access_token)
                return unencrypted_access_token

            encrypted_refresh_token = oauth_info.refresh_token_encrypted
            unencrypted_refresh_token = self.encryption_service.decrypt(encrypted_refresh_token)

            updated_tokens = await self.twitch_access_token_updater.get_new_access_and_refresh_tokens(
                unencrypted_refresh_token
            )

            update_oauth_connection_command = UpdateOAuthConnectionCommand(
                user_id=user_id,
                access_token_encrypted=self.encryption_service.encrypt(updated_tokens["access_token"]),
                refresh_token_encrypted=self.encryption_service.encrypt(updated_tokens["refresh_token"]),
                access_token_expires_at=updated_tokens["access_token_expires_at"],
            )

            await uow.oauth_connections_repository.update()

            return None

    def is_token_expired(
        self,
        token_expiration_at: datetime,
        current_time: datetime,
    ) -> bool:

        if token_expiration_at.tzinfo is None:
            token_expiration_at = token_expiration_at.replace(tzinfo=timezone.utc)

        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        return current_time >= token_expiration_at
