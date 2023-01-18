from fastapi import status

from package.exceptions.InvalidData.InvalidDataException import InvalidDataException
from package.routes.chat.inputs.CreateInput import CreateInput

USER_NOT_EXISTS_MESSAGE = "User with given ID does not exist"
CHAT_WITH_YOURSELF_MESSAGE = "You can not create a chat with yourself"

user_not_exists = InvalidDataException[CreateInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="USER_NOT_EXISTS",
    message=USER_NOT_EXISTS_MESSAGE,
).populate_errors_with_message()

chat_with_yourself = InvalidDataException[CreateInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="CHAT_WITH_YOURSELF",
    message=CHAT_WITH_YOURSELF_MESSAGE,
).populate_errors_with_message()
