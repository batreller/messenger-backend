from fastapi import APIRouter, Depends

from package.auth import auth_injector
from package.db.models.Chat import Chat
from package.db.models.ChatMessage import Message
from package.db.models.User import User
from package.routes.chat.exceptions import (
    chat_not_accessible,
    chat_or_message_not_exists,
)
from package.routes.chat.inputs.DeleteMessageInput import DeleteMessageInput

router = APIRouter()


@router.delete('/message')
async def delete_message(data: DeleteMessageInput, user: User = Depends(auth_injector)):
    chat = await Chat.get(id=data.chat_id)
    # TODO: raise here 403 forbidden
    if chat.first_user_id != user.id and chat.second_user_id != user.id:
        raise chat_not_accessible

    # TODO: maybe replace to validators if its possible - https://github.com/pydantic/pydantic/issues/857
    chat_message = await Message.get_or_none(id=data.message_id, chat_id=data.chat_id)
    if not chat_message:
        raise chat_or_message_not_exists

    await Message.filter(
        id=data.message_id,
        chat_id=data.chat_id,
    ).delete()

    return {"success": True}
