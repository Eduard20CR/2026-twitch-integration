from enum import StrEnum


class WsEvents(StrEnum):
    PING = "ping"
    CHAT_MESSAGE = "chat_message"
    JOIN_ROOM = "join_room"
    INFO_MESSAGE = "info_message"
