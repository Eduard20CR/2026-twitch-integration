class AppException(Exception):

    status_code = 500
    error_code = "internal_error"

    def __init__(self, message: str):
        self.message = message

        super().__init__(message)
