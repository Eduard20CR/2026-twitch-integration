from fastapi import APIRouter, Request, HTTPException

from .controller import AuthController
from .service import AuthService
from .exceptions import OAuthException

auth_router = APIRouter(prefix="/auth")

service = AuthService()
controller = AuthController(service=service)


@auth_router.get("/login")
async def login(request: Request):
    return await controller.login(request)


@auth_router.get("/callback")
async def callback(request: Request):
    try:
        return await controller.callback(request)
    except OAuthException:
        raise HTTPException(status_code=401, detail="OAuth failed")
