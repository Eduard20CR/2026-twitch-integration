import os
from dotenv import load_dotenv
import httpx

load_dotenv()

token = "j8xjpdgttajihvgx3tehiveea46ow9"


def get_token():
    client_id = os.getenv("TWITCH_CLIEND_ID")
    client_secret = os.getenv("TWITCH_CLIEND_SECRET")

    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret}")

    response = httpx.post(
        "https://id.twitch.tv/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        },
    )

    print(response.status_code)
    print(response.json())


def get_user_info():
    response = httpx.get(
        f"https://api.twitch.tv/helix/users?login=scarus_",
        headers={
            "Client-ID": os.getenv("TWITCH_CLIEND_ID"),
            "Authorization": f"Bearer {token}",
        },
    )

    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    get_user_info()
