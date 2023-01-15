from fastapi import Header
from pydantic import BaseModel

from package.auth.exceptions import credentials_exception
from package.auth.get_current_user import get_current_user
from package.db.models.User import User


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


async def auth_injector(
        token: str | None = Header(default=None, alias='Authorization')
) -> User:
    if token is None:
        raise credentials_exception

    token_type, token = token.split(' ')

    if token_type != 'Bearer':
        raise credentials_exception

    return await get_current_user(token)
