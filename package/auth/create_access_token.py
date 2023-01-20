from datetime import datetime, timedelta
from typing import Any, TypedDict

from jose import jwt

from package.config import config


class TokenPayloadDict(TypedDict):
    user_id: int


def create_access_token(
    payload: TokenPayloadDict,
    expires_delta: timedelta = timedelta(minutes=config.jwt.expiry_time_minutes)
) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode: dict[str, Any] = {
        "sub": str(payload['user_id']),
        "exp": expire
    }

    encoded_jwt = jwt.encode(
        to_encode,
        config.jwt.secret,
        algorithm=config.jwt.algorithm
    )

    return encoded_jwt
