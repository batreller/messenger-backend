from pydantic import BaseModel, Field


class RegisterInput(BaseModel):
    username: str = Field(max_length=64)
    email: str = Field(max_length=255)
    password: str = Field(max_length=2047)
