from common.logging.logger import logger
from fastapi.responses import JSONResponse


async def global_exception_handler(request, exc: Exception):

    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_SERVER_ERROR", "detail": "Unexpected error"},
    )
