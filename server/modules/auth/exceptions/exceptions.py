class OAuthException(Exception):
    """Error genérico de OAuth (Twitch, Google, etc.)"""

    pass


class TwitchAuthenticationError(Exception):
    pass


class UserCreationError(Exception):
    """Error al crear un usuario en la base de datos"""

    pass


class SessionCreationError(Exception):
    """Error al crear una sesión en la base de datos"""

    pass


class OAuthConnectionCreationError(Exception):
    """Error al crear una sesión en la base de datos"""

    pass


class OAuthConnectionNotFound(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"OAuth connection not found for user {user_id}")
