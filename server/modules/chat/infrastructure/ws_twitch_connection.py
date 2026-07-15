class WsTwitchConnection:

    def __init__(self, token: str, channel: str):
        self.token = token
        self.channel = channel
        self.connected = False

    async def connect(self):
        # Logic to establish a connection to Twitch
        pass

    async def disconnect(self):
        # Logic to disconnect from Twitch
        pass
