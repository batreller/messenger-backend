from fastapi import APIRouter
from fastapi import Depends
from tortoise.expressions import Q

from package.auth import auth_injector
from package.db.models.Chat import Chat
from package.db.models.User import User
from package.routes.chat.exceptions import chat_with_yourself
from package.routes.chat.inputs.CreateInput import CreateInput

router = APIRouter()


@router.post('/create')
async def create(data: CreateInput, user: User = Depends(auth_injector)):
    # TODO: may be deleted
    if data.user_id == user.id:
        raise chat_with_yourself

    chat = await Chat.get_or_none(
        Q(first_user_id=user.id, second_user_id=data.user_id)
        |
        Q(first_user_id=user.id, second_user_id=user.id)
    )

    # return the chat if its already created
    if chat:
        return chat

    # if the chat is not created - create it and return a new chat
    new_chat = await Chat.create(
        first_user_id=user.id,
        second_user_id=data.user_id,
    )

    await new_chat.save()
    return new_chat
