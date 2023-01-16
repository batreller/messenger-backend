from fastapi import status
from pydantic import Field

from package.exceptions.InvalidData.InvalidDataException import InvalidDataException
from package.routes.user.inputs.LoginInput import LoginInput
from package.routes.user.inputs.RegisterInput import RegisterInput


class PartialRegister(RegisterInput):
    password: str | None = Field(required=False, default=None)


user_exists_message = "This user already exists."
user_exists = InvalidDataException[PartialRegister](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="USER_EXISTS",
    message=user_exists_message,
    field_error_mapping=PartialRegister(
        username=user_exists_message,
        email=user_exists_message,
    )
).populate_errors_with_message()


wrong_credentials = InvalidDataException[LoginInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="WRONG_CREDENTIALS",
    message="Wrong login credential, try again."
).populate_errors_with_message()
