from fastapi import Depends

from package.auth import auth_injector
from package.db.models.Chat import Chat
from package.injectors.chat_participant_of import chat_participant_of


async def messages(
    chat: Chat = Depends(chat_participant_of)
):
    # FIXME: Paginaton?
    # TODO: Maybe we should utilize a propery pydantic model as a typing for the response
    messages = await chat.messages.all()
    return {
        "messages": messages
    }
