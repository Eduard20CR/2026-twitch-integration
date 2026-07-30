from pydantic import BaseModel


class TwitchUserInformationResponse(BaseModel):
    email: str
    profile_image_url: str
