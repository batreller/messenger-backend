from fastapi import Depends

from package.auth import auth_injector
from package.db.models.Chat import Chat
from package.db.models.Message import Message
from package.db.models.User import User
from package.injectors.chat_participant_of import chat_participant_of
from package.routes.chat.inputs.SendMessageInput import SendMessageInput


async def send_message(
    data: SendMessageInput,
    user: User = Depends(auth_injector),
    chat: Chat = Depends(chat_participant_of),
):
    new_message = await Message.create(
        chat_id=chat.id,
        author_id=user.id,
        contents=data.contents
    )

    return new_message
