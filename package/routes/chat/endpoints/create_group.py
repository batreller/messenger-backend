from fastapi import Depends

from package.auth import auth_injector
from package.db.models.Chat import Chat, ChatType, PublicChatWithParticipants
from package.db.models.User import User
from package.routes.chat.exceptions import chat_with_yourself, user_does_not_exist
from package.routes.chat.inputs.CreateGroupInput import CreateGroupInput


async def create_group(
    data: CreateGroupInput,
    user: User = Depends(auth_injector)
) -> PublicChatWithParticipants:
    if user.id in data.with_ids:
        raise chat_with_yourself

    chatting_with = await User.filter(
        id__in=data.with_ids
    )

    if len(chatting_with) != len(data.with_ids):
        raise user_does_not_exist

    new_chat = await Chat.create(
        name=data.name,
        creator=user,
        type=ChatType.group
    )

    await new_chat.participants.add(user, *chatting_with)

    return await new_chat.public_with_participants()

