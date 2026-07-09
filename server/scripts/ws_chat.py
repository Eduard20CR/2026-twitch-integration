import asyncio
import os
from dotenv import load_dotenv
import websockets


load_dotenv()

TWITCH_WS_URL = "wss://irc-ws.chat.twitch.tv:443"

ACCESS_TOKEN = "k2k3rizhdeioilt70u1dmx6enypsyg"
USERNAME = "scarus_"
CHANNEL = "scarus_"


async def connect():
    async with websockets.connect(TWITCH_WS_URL) as ws:
        print("Connected!")

        # Autenticación IRC
        await ws.send(f"PASS oauth:{ACCESS_TOKEN}")
        await ws.send(f"NICK {USERNAME}")

        # Opcional pero recomendado
        await ws.send("CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership")

        # Entrar al canal
        await ws.send(f"JOIN #{CHANNEL}")

        print(f"Joined #{CHANNEL}")

        while True:
            message = await ws.recv()

            print(message)

            # Twitch envía PING periódicamente.
            # Si no respondes con PONG te desconecta.
            if message.startswith("PING"):
                pong = message.replace("PING", "PONG", 1)
                await ws.send(pong)
                print(">>", pong)


if __name__ == "__main__":
    asyncio.run(connect())