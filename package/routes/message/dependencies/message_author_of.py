from fastapi import Depends, Path

from package.auth import auth_injector
from package.db.models.Message import Message
from package.db.models.User import User
from package.routes.message.exceptions import message_does_not_exist, not_the_owner


async def message_author_of(
    message_id: int = Path(),
    user: User = Depends(auth_injector)
) -> Message:
    predicate = await Message.get_or_none(
        id=message_id
    ).prefetch_related('author')

    if predicate is None:
        raise message_does_not_exist

    if predicate.author.id != user.id:
        raise not_the_owner

    return predicate
