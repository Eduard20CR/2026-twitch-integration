from pydantic import BaseModel


class TwitchUserInformation(BaseModel):
    email: str
    profile_image_url: str
