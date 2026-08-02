from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    username: str
    email: str
    sub: str
    provider: str
    profile_image_url: str
