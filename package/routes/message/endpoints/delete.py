from fastapi import Depends

from package.db.models.Message import Message
from package.injectors.message_author_of import message_author_of


async def delete(message: Message = Depends(message_author_of)):
    await message.delete()

    return {"success": True}
