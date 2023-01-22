from fastapi import Depends

from package.auth import auth_injector
from package.db.models.User import User


async def me(user: User = Depends(auth_injector)):
    return user.public()
