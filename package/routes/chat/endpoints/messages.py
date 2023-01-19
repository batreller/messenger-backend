from fastapi import APIRouter, Depends
from tortoise.expressions import Q

from package.auth import auth_injector
from package.db.models.Chat import Chat
from package.db.models.ChatMessage import Message
from package.db.models.User import User
from package.routes.chat.exceptions import chat_not_accessible
from package.routes.chat.inputs.MessagesInput import MessagesInput

router = APIRouter()


@router.get('/messages')
async def get_messages(data: MessagesInput, user: User = Depends(auth_injector)):
    chat = await Chat.get_or_none(id=data.chat_id)
    if not chat:
        raise chat_not_accessible

    # TODO: raise here 403 forbidden
    if chat.first_user_id != user.id and chat.second_user_id != user.id:
        raise chat_not_accessible

    all_messages = await Message.filter(chat_id=data.chat_id).all()

    return all_messages
