from fastapi import APIRouter
from fastapi import Depends

from package.auth import auth_injector
from package.db.models.ChatMessage import ChatMessage
from package.db.models.User import User
from package.db.models.Chat import Chat
from package.routes.chat.inputs.DeleteMessageInput import DeleteMessageInput
from package.routes.chat.exceptions import chat_or_message_not_exists
from package.routes.chat.exceptions import chat_not_accessible
router = APIRouter()


@router.delete('/message')
async def delete_message(data: DeleteMessageInput, user: User = Depends(auth_injector)):
    chat = await Chat.get(id=data.chat_id)
    # todo raise here 403 forbidden
    if chat.first_user_id != user.id and chat.second_user_id != user.id:
        raise chat_not_accessible

    # todo maybe replace to validators if its possible - https://github.com/pydantic/pydantic/issues/857
    chat_message = await ChatMessage.get_or_none(id=data.message_id, chat_id=data.chat_id)
    if not chat_message:
        raise chat_or_message_not_exists

    await ChatMessage.filter(
        id=data.message_id,
        chat_id=data.chat_id,
    ).delete()

    return {"success": True}
