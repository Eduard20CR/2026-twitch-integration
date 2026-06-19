from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth

from fastapi import FastAPI
from routers import auth_router
from routers import chat_router

load_dotenv()

oauth = OAuth(
    name="twitch",
    client_id='TU_CLIENT_ID_DE_TWITCH',
    client_secret='TU_CLIENT_SECRET',
    server_metadata_url='https://id.twitch.tv/oauth2/.well-known/openid-configuration', # OIDC Discovery
    client_kwargs={'scope': 'openid user:read:email chat:read'},
)


app = FastAPI(lifespan=chat_router.lifespan)

app.include_router(auth_router.router)

