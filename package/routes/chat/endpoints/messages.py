from fastapi import Depends
from pydantic import BaseModel

from package.db.models.Chat import Chat
from package.db.models.Message import PublicMessage
from package.routes.chat.dependencies.chat_participant_of import chat_participant_of


class MessagesList(BaseModel):
    messages: list[PublicMessage]


# TODO: Paginaton?
async def messages(
    chat: Chat = Depends(chat_participant_of)
) -> MessagesList:
    messages = []
    async for message in chat.messages.all().prefetch_related('author'):
        messages.append(await message.public())

    return MessagesList(
        messages=messages
    )