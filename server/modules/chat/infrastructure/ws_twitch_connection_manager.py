class WsTwitchConnectionManager:
    def __init__(self):
        self.connections = {}

    def add_connection(self, user_id, connection):
        self.connections[user_id] = connection

    def remove_connection(self, user_id):
        if user_id in self.connections:
            del self.connections[user_id]

    def get_connection(self, user_id):
        return self.connections.get(user_id)


ws_twitch_connection_manager = WsTwitchConnectionManager()
