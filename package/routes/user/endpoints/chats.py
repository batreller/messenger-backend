from fastapi import Depends

from package.auth import auth_injector
from package.db.models.User import User


# TODO: Add pagination
async def chats(user: User = Depends(auth_injector)):
    user_chats = await user.chats.all()

    return user_chats
