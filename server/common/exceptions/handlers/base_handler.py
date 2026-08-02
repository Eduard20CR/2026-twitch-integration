from common.exceptions.base import AppException
from fastapi.responses import JSONResponse


async def app_exception_handler(request, exc: AppException):

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code, "detail": exc.message},
    )
