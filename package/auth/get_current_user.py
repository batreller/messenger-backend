from package.auth.decode_access_token import decode_access_token
from package.auth.exceptions import credentials_exception
from package.db.models.User import User


async def get_current_user(token: str) -> User:
    token_payload = decode_access_token(token)

    user = await User.filter(id=token_payload.user_id).first()
    if user is None:
        raise credentials_exception

    return user
