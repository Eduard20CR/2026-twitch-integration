from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    username: str
    email: str
    sub: str
    provider: str
