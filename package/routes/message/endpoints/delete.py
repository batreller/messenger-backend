from fastapi import Depends

from package.db.models.Message import Message
from package.routes.message.dependencies.message_author_of import message_author_of
from package.shared.SuccessResponse import SuccessResponse


async def delete(
    message: Message = Depends(message_author_of)
) -> SuccessResponse:
    await message.delete()

    return SuccessResponse()
