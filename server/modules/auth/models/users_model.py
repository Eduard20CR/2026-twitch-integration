from uuid import uuid4, UUID

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    email: str
    sub: str = Field(index=True)
    provider: str
    profile_image_url: str
