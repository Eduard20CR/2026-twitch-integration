# common/exceptions/database.py

from common.exceptions.base import AppException


class DatabaseError(AppException):

    status_code = 500
    error_code = "DATABASE_ERROR"


class DatabaseConnectionError(DatabaseError):

    error_code = "DATABASE_CONNECTION_ERROR"


class DatabaseIntegrityError(DatabaseError):

    error_code = "DATABASE_INTEGRITY_ERROR"
