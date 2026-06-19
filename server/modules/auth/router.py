import os

from dotenv import load_dotenv

from fastapi import APIRouter, Request, HTTPException
from common.auth.auth import oauth

load_dotenv()

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/login")
async def login(request: Request):
    return await oauth.twitch.authorize_redirect(request, os.getenv("REDIRECT_URL"))


@auth_router.get("/callback")
async def callback(request: Request):
    try:
        token = await oauth.twitch.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=401, detail="OAuth failed")

    return token
