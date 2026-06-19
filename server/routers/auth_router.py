from fastapi import APIRouter, Request, HTTPException
import httpx

from common.auth.auth import oauth

router = APIRouter(prefix="/auth")


@router.get("/login")
async def login(request: Request):

    redirect_uri = "http://localhost:8000/auth/callback/"

    return await oauth.twitch.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def callback(request: Request):

    try:
        token = await oauth.twitch.authorize_access_token(request)

    except Exception:
        raise HTTPException(status_code=401, detail="OAuth failed")

    return {"token": token}
