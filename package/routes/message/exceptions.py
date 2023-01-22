from fastapi import status

from package.exceptions.CustomException import CustomException

MESSAGE_DOES_NOT_EXIST_MESSAGE = "Message doesn't exist."
NOT_THE_OWNER_MESSAGE = "You are not the owner of the message. You can't delete it."

message_does_not_exist = CustomException(
    status_code=status.HTTP_404_NOT_FOUND,
    message=MESSAGE_DOES_NOT_EXIST_MESSAGE,
    code='MESSAGE_DOES_NOT_EXIST'
)

not_the_owner = CustomException(
    status_code=status.HTTP_403_FORBIDDEN,
    message=NOT_THE_OWNER_MESSAGE,
    code="NOT_THE_OWNER"
)