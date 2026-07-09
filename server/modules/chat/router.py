import asyncio
import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from common.dependencies.get_current_user_ws import get_current_user_ws
from modules.chat.ws.ws_connection import WsConnection
from modules.chat.ws.ws_manager import ws_manager

chat_router = APIRouter(prefix="/api/chat")


@chat_router.websocket("")
async def websocket_endpoint(websocket: WebSocket, current_user=Depends(get_current_user_ws)):
    await websocket.accept()

    ws_connection = WsConnection(websocket, current_user.get("user_id"))

    receiver = asyncio.create_task(receive_messages(ws_connection, current_user))

    ping_sender = asyncio.create_task(send_ping(ws_connection))

    done, pending = await asyncio.wait([receiver, ping_sender], return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    print("Connection closed")


async def send_ping(ws_connection: WsConnection):
    while True:
        await asyncio.sleep(15)
        await ws_connection.websocket.send_text("ping keep alive")


async def receive_messages(ws_connection: WsConnection, current_user):
    try:
        while True:
            message = await ws_connection.websocket.receive_text()
            json_message = json.loads(message)

            event = json_message.get("event")
            payload = json_message.get("payload")

            print(f"{ws_connection.id}: {message}")

            match event:
                case "connect_to_chat_room":
                    ws_manager.add_user_to_room(ws_connection.user_id, ws_connection)

                case "leave_chat_room":
                    ws_manager.remove_user_from_room(ws_connection.user_id, ws_connection.user_id)

                case "pong":
                    print(f"Received pong from {ws_connection.id}")
                    pass

                case _:
                    print(f"Unknown event: {event}")

    except WebSocketDisconnect:
        print(f"{ws_connection.id} disconnected")
