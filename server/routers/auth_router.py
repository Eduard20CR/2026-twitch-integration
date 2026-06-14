
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse
import httpx

load_dotenv()

router = APIRouter()

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")
token_url = os.getenv("TOKEN_URL")
redirect_uri = os.getenv("REDIRECT_URI")
redirect_url = os.getenv("REDIRECT_URL")

@router.get("/auth" ,tags=["authentication"])
async def auth(code: str, state: str):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    async with httpx.AsyncClient() as client:
        twitch_response = await client.post(
            token_url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    try:
        twitch_response.raise_for_status()
    except httpx.HTTPStatusError:
        raise httpx.HTTPStatusError(
            "Token exchange failed",
            request=twitch_response.request,
            response=twitch_response
        )
        
    json_response = twitch_response.json()
    access_token = json_response.get("access_token")
    
    response = RedirectResponse(redirect_url, status_code=status.HTTP_308_PERMANENT_REDIRECT)    
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,   
        secure=True,     
        samesite="lax"
    )
        
    return response
