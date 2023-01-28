import re
from typing import Generic, TypeVar
from unittest import TestCase

from package.auth import TokenResponse, get_current_user
from package.db.models.User import User
from package.routes.user.inputs.LoginInput import LoginInput
from package.routes.user.inputs.RegisterInput import RegisterInput

DataContainer = TypeVar('DataContainer', LoginInput, RegisterInput)

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class ValidatingTokenResponse(Generic[DataContainer], TokenResponse):
    async def validate_user(
        self,
        input_data: DataContainer,
        ommited_fields: list[str] | None = None
    ) -> User:
        if ommited_fields is None:
            ommited_fields = ['password']

        assert self.token_type.lower() == 'bearer'
        authenticated_user = await get_current_user(self.access_token)

        to_check = {}
        if isinstance(input_data, RegisterInput):
            to_check = input_data.dict()
        if isinstance(input_data, LoginInput):
            is_email = EMAIL_REGEX.match(input_data.usernameOrEmail) is not None
            key_name = 'email' if is_email else 'username'
            to_check = {
                key_name: input_data.usernameOrEmail
            }

        for field in ommited_fields:
            to_check.pop(field, None)

        needed_data = {key: getattr(authenticated_user, key) for key in to_check.keys()}
        TestCase().assertDictEqual(to_check, needed_data)

        return authenticated_user
