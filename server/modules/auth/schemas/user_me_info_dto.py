from pydantic import BaseModel


class UserMeInfoDTO(BaseModel):
    username: str
    email: str
    profile_image_url: str
