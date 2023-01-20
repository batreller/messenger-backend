from fastapi import status

from package.exceptions.CustomException import CustomException
from package.exceptions.InvalidData.InvalidDataException import InvalidDataException
from package.routes.chat.inputs.CreatePrivateInput import CreatePrivateInput

# TODO: I should do something about...
USER_NOT_EXISTS_MESSAGE = "User with given ID does not exist"
CHAT_EXISTS_MESSAGE = 'A private chat with this person already exists. You can not create another one.'
CHAT_WITH_YOURSELF_MESSAGE = "You can not create a chat with yourself"
CHAT_DOES_NOT_EXIST_MESSAGE = "This chat doesn't exist."

user_does_not_exist = InvalidDataException[CreatePrivateInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="USER_NOT_EXISTS",
    message=USER_NOT_EXISTS_MESSAGE,
).populate_errors_with_message()

chat_with_yourself = InvalidDataException[CreatePrivateInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="CHAT_WITH_YOURSELF",
    message=CHAT_WITH_YOURSELF_MESSAGE,
).populate_errors_with_message()

chat_exists = CustomException(
    status_code=status.HTTP_403_FORBIDDEN,
    code="CHAT_EXISTS",
    message=CHAT_EXISTS_MESSAGE
)

chat_does_not_exist = CustomException(
    status_code=status.HTTP_404_NOT_FOUND,
    code='CHAT_DOES_NOT_EXIST',
    message=CHAT_DOES_NOT_EXIST_MESSAGE
)