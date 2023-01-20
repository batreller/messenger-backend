from fastapi import Depends, Path

from package.auth import auth_injector
from package.db.models.Chat import Chat
from package.db.models.User import User
from package.routes.chat.exceptions import chat_does_not_exist


# TODO: I think I should move these files to the corresponding folders under the routes derictory...
async def chat_participant_of(
    chat_id: int = Path(),
    user: User = Depends(auth_injector)
) -> Chat:
    predicate = await Chat.get_or_none(
        id=chat_id
    )

    if predicate is None:
        raise chat_does_not_exist

    is_participant = await predicate.participants.filter(
        id=user.id
    ).exists()

    if not is_participant:
        raise chat_does_not_exist

    return predicate