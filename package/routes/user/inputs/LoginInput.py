from pydantic import BaseModel, Field


class LoginInput(BaseModel):
    usernameOrEmail: str = Field(max_length=64)
    password: str = Field(max_length=2047)
