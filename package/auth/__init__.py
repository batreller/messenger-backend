from fastapi import Depends, Header
from pydantic import BaseModel

from package.auth.decode_access_token import decode_access_token
from package.auth.exceptions import credentials_exception
from package.auth.get_current_user import get_current_user
from package.db.models.User import User


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def parse_authorization_header(
    token: str | None = Header(default=None, alias='Authorization')
) -> str:
    if token is None:
        raise credentials_exception

    token_type, token = token.split(' ')

    if token_type != 'Bearer':
        raise credentials_exception

    return token


async def auth_injector(
    token: str = Depends(parse_authorization_header)
) -> User:
    return await get_current_user(token)


async def auth_id(
    token: str = Depends(parse_authorization_header)
) -> int:
    token_payload = decode_access_token(token)
    if token_payload.user_id is None:
        raise credentials_exception

    return token_payload.user_id
