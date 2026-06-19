
import os

from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth

load_dotenv()

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")

oauth = OAuth()

oauth.register(
    name="twitch",
    client_id=client_id,
    client_secret=client_secret,
    # server_metadata_url='https://id.twitch.tv/oauth2/.well-known/openid-configuration', 
    access_token_url="https://id.twitch.tv/oauth2/token",
    authorize_url="https://id.twitch.tv/oauth2/authorize",
    client_kwargs={
        "scope": "openid user:read:email"
    }
)