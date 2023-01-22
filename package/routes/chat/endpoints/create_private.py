from fastapi import Depends

from package.auth import auth_injector
from package.db.models.Chat import Chat, ChatType, PublicChatWithParticipants
from package.db.models.User import User
from package.routes.chat.exceptions import (
    chat_exists,
    chat_with_yourself,
    user_does_not_exist,
)
from package.routes.chat.inputs.CreatePrivateInput import CreatePrivateInput


async def create_private(
    data: CreatePrivateInput,
    user: User = Depends(auth_injector)
) -> PublicChatWithParticipants:
    if data.with_user_id == user.id:
        raise chat_with_yourself

    chat_with_predicate = await User.get_or_none(
        id=data.with_user_id
    )

    if chat_with_predicate is None:
        raise user_does_not_exist

    chat = await Chat.filter(
        participants__id__in=[user.id, chat_with_predicate.id],
        creator=user,
        type=ChatType.private
    ).first()

    if chat is not None:
        raise chat_exists

    new_chat = await Chat.create(
        type=ChatType.private
    )

    await new_chat.participants.add(
        user,
        chat_with_predicate
    )

    return await new_chat.public_with_participants()
