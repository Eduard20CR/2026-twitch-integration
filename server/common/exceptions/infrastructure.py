from common.exceptions.database import AppException


class InfrastructureException(AppException):

    status_code = 500
    error_code = "infrastructure_error"
