from common.exceptions.base import AppException


class OAuthException(Exception):
    """Error genérico de OAuth (Twitch, Google, etc.)"""

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


class OAuthConnectionNotFound(AppException):
    status_code = 404
    error_code = "OAUTH_CONNECTION_NOT_FOUND"

    def __init__(self, user_id):
        super().__init__(f"OAuth connection not found for user {user_id}")
