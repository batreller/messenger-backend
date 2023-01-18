from fastapi import status

from package.exceptions.InvalidData.InvalidDataException import InvalidDataException
from package.exceptions import CustomException
from package.routes.chat.inputs.CreateInput import CreateInput
from package.routes.chat.inputs.DeleteMessageInput import DeleteMessageInput
from package.routes.chat.inputs.CreateInput import CreateInput

USER_NOT_EXISTS_MESSAGE = "User with given ID does not exist"
CHAT_WITH_YOURSELF_MESSAGE = "You can not create a chat with yourself"
ACCESS_DENIED_MESSAGE = "The chat you are trying to access is not accessible"
CHAT_OR_MESSAGE_NOT_EXISTS_MESSAGE = "The chat or message are trying to access is not accessible"

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

chat_or_message_not_exists = InvalidDataException[DeleteMessageInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="CHAT_OR_MESSAGE_NOT_EXISTS",
    message=CHAT_OR_MESSAGE_NOT_EXISTS_MESSAGE,
).populate_errors_with_message()

chat_not_accessible = InvalidDataException[DeleteMessageInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="ACCESS_DENIED",
    message=ACCESS_DENIED_MESSAGE,
).populate_errors_with_message()
