from fastapi import APIRouter
from fastapi import Depends
from tortoise.expressions import Q

from package.auth import auth_injector
from package.db.models.Chat import Chat
from package.db.models.User import User

router = APIRouter()


@router.get('/chats')
async def chats(user: User = Depends(auth_injector)):
    user_chats = await Chat.filter(
        Q(first_user_id=user.id)
        |
        Q(second_user_id=user.id)
    ).all()

    return user_chats
