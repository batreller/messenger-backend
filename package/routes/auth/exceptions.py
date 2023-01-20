from fastapi import status
from pydantic import Field

from package.exceptions.CustomException import CustomException
from package.exceptions.InvalidData.InvalidDataException import InvalidDataException
from package.routes.user.inputs.LoginInput import LoginInput
from package.routes.user.inputs.RegisterInput import RegisterInput


class PartialRegister(RegisterInput):
    password: str | None = Field(required=False, default=None)


USER_EXISTS_MESSAGE = "This user already exists."
WRONG_CREDENTIALS_MESSAGE = "Wrong login credential, try again."
ALREADY_AUTH_MESSAGE = 'You are already authenicated. You have to logout first'

user_exists = InvalidDataException[PartialRegister](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="USER_EXISTS",
    message=USER_EXISTS_MESSAGE,
    field_error_mapping=PartialRegister(
        username=USER_EXISTS_MESSAGE,
        email=USER_EXISTS_MESSAGE,
    )
).populate_errors_with_message()

wrong_credentials = InvalidDataException[LoginInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="WRONG_CREDENTIALS",
    message=WRONG_CREDENTIALS_MESSAGE
).populate_errors_with_message()

already_authenticated = CustomException(
    status_code=status.HTTP_403_FORBIDDEN,
    code="ALREADY_AUTHENICATED",
    message=ALREADY_AUTH_MESSAGE
)
