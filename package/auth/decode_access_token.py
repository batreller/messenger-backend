from jose import JWTError, jwt
from pydantic import BaseModel

from package.auth import credentials_exception
from package.config import config


class TokenPayload(BaseModel):
    user_id: int | None = None


def decode_access_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            config.jwt.secret,
            algorithms=[config.jwt.algorithm]
        )

        if payload is None:
            raise credentials_exception

        user_id = int(payload.get('sub', None))

        if user_id is None:
            raise credentials_exception

        token_payload = TokenPayload(user_id=user_id)

        return token_payload
    except JWTError:
        raise credentials_exception
