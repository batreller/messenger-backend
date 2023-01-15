from pydantic import BaseModel


class LoginInput(BaseModel):
    usernameOrEmail: str
    password: str
