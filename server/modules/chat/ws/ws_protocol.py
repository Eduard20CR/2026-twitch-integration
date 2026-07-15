from modules.chat.domain.ws_message import WsMessage
from modules.chat.domain.ws_events import WsEvents


class WsProtocol:

    @staticmethod
    def ping():
        return WsMessage(event=WsEvents.PING, payload={})

    @staticmethod
    def chat_message(message: str):
        return WsMessage(event=WsEvents.CHAT_MESSAGE, payload={"message": message})
