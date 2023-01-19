from fastapi import APIRouter, Depends

from package.auth import auth_injector
from package.db.models.Chat import Chat
from package.db.models.ChatMessage import Message
from package.db.models.User import User
from package.routes.chat.exceptions import chat_not_accessible
from package.routes.chat.inputs.SendMessageInput import SendMessageInput

router = APIRouter()


@router.post('/message')
async def send_message(data: SendMessageInput, user: User = Depends(auth_injector)):
    chat = await Chat.get_or_none(id=data.chat_id)
    if not chat:
        raise chat_not_accessible

    # TODO: raise here 403 forbidden
    if chat.first_user_id != user.id and chat.second_user_id != user.id:
        raise chat_not_accessible

    new_chat_message = await Message.create(
        chat_id=data.chat_id,
        author_id=user.id,
        contents=data.text
    )

    await new_chat_message.save()
    return new_chat_message
