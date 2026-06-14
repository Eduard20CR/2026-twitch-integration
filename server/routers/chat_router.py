
import asyncio
import os

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.concurrency import asynccontextmanager
import websockets

load_dotenv()

router = APIRouter()

ws_url = os.getenv("WS_URL")

connection = None

@router.post("/connect", tags=["chat"])
async def connect():
    global connection
    
    if connection is None:
         async with websockets.connect(ws_url) as websocket:
                
                
                
                while True:
                    message = await websocket.recv()
                    print(message)
                    

        
    return {"message": connection}




class TwitchWebSocket:
    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.url)
            await self.websocket.send("PASS oauth:6izrlbcjh7yl5xiom8xds134ebdnkb")
            await self.websocket.send("NICK scarus_")
            await self.websocket.send("JOIN #scarus_")
        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")

    async def listen(self):
        while True:
            message = await self.websocket.recv()
            parsed_message = self.parse_message(message)
            print(message)
            
    def parse_message(self, message):
        # Implement your message parsing logic here
        pass

async def twitch_listener():
    twitch_web_socket = TwitchWebSocket(ws_url)
    await twitch_web_socket.connect()
    await twitch_web_socket.listen()
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    # task = asyncio.create_task(twitch_listener())

    yield

    # task.cancel()
    print("Conexión cerrada y recursos liberados.")