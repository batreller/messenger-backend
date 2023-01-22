from fastapi import Depends

from package.db.models.Chat import Chat, PublicChatWithParticipants
from package.routes.chat.dependencies.chat_participant_of import chat_participant_of


async def chat(
    chat: Chat = Depends(chat_participant_of)
) -> PublicChatWithParticipants:
    return await chat.public_with_participants()