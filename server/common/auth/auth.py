import os

from authlib.integrations.starlette_client import OAuth

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")
server_metadata_url = os.getenv("TWITCH_SERVER_METADATA_URL")
access_token_url = os.getenv("TWITCH_ACCESS_TOKEN_URL")
authorize_url = os.getenv("TWITCH_AUTHORIZE_URL")

oauth = OAuth()

oauth.register(
    name="twitch",
    client_id=client_id,
    client_secret=client_secret,
    server_metadata_url=server_metadata_url,
    access_token_url=access_token_url,
    authorize_url=authorize_url,
    client_kwargs={
        "scope": "openid chat:read chat:edit",
        "token_endpoint_auth_method": "client_secret_post",
    },
)
