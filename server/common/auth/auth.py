import os

from authlib.integrations.starlette_client import OAuth

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")

oauth = OAuth()

oauth.register(
    name="twitch",
    client_id=client_id,
    client_secret=client_secret,
    server_metadata_url="https://id.twitch.tv/oauth2/.well-known/openid-configuration",
    access_token_url="https://id.twitch.tv/oauth2/token",
    authorize_url="https://id.twitch.tv/oauth2/authorize",
    client_kwargs={
        "scope": "openid chat:read chat:edit",
        "token_endpoint_auth_method": "client_secret_post",
    },
)
