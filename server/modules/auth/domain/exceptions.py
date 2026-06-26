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
