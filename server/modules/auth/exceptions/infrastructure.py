from common.exceptions.infrastructure import InfrastructureException


class TwitchApiException(InfrastructureException):

    status_code = 502
    error_code = "twitch_api_error"

    def __init__(
        self,
        message: str = "Twitch API error",
    ):
        super().__init__(message)


class TwitchTimeoutError(TwitchApiException):

    status_code = 504
    error_code = "twitch_timeout"

    def __init__(
        self,
        message: str = "Twitch API request timed out",
    ):
        super().__init__(message)


class TwitchConnectionError(TwitchApiException):

    status_code = 503
    error_code = "twitch_connection_error"

    def __init__(
        self,
        message: str = "Could not connect to Twitch API",
    ):
        super().__init__(message)


class TwitchTokenExpired(TwitchApiException):

    status_code = 401
    error_code = "twitch_token_expired"

    def __init__(
        self,
        message: str = "Twitch access token expired",
    ):
        super().__init__(message)


class TwitchRateLimitExceeded(TwitchApiException):

    status_code = 429
    error_code = "twitch_rate_limit_exceeded"

    def __init__(
        self,
        message: str = "Twitch API rate limit exceeded",
    ):
        super().__init__(message)


class TwitchAuthenticationError(TwitchApiException):

    status_code = 401
    error_code = "twitch_authentication_error"

    def __init__(
        self,
        message: str = "Failed to authenticate with Twitch",
    ):
        super().__init__(message)
