class OAuthException(Exception):
    """Error genérico de OAuth (Twitch, Google, etc.)"""

    pass


class TwitchAuthenticationError(Exception):
    pass
