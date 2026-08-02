from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from common.exceptions.database import (
    DatabaseError,
    DatabaseIntegrityError,
)


def handle_database_errors(func):

    async def wrapper(*args, **kwargs):

        try:
            return await func(*args, **kwargs)

        except IntegrityError as e:
            raise DatabaseIntegrityError("Database integrity error") from e

        except SQLAlchemyError as e:
            raise DatabaseError("Database operation failed") from e

    return wrapper
