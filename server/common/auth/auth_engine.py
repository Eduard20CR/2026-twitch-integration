from authlib.integrations.starlette_client import OAuth

from common.env.settings import settings

oauth = OAuth()

oauth.register(
    name="twitch",
    client_id=settings.twitch_client_id,
    client_secret=settings.twitch_client_secret,
    server_metadata_url=settings.twitch_server_metadata_url,
    access_token_url=settings.twitch_access_token_url,
    authorize_url=settings.twitch_authorize_url,
    client_kwargs={
        "scope": "openid user:read:email user:read:chat user:bot channel:bot",
        "token_endpoint_auth_method": "client_secret_post",
    },
)
