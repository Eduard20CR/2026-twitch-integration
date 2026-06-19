from fastapi import APIRouter, Request, HTTPException
from .service import AuthService
from .exceptions import OAuthException

auth_router = APIRouter(prefix="/auth")

service = AuthService()


@auth_router.get("/login")
async def login(request: Request):
    return await service.get_login_redirect(request)


@auth_router.get("/callback")
async def callback(request: Request):
    try:
        return await service.handle_callback(request)

    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")
