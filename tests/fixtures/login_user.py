from typing import Literal, Protocol

import pytest
from httpx import AsyncClient, Response
from pydantic import BaseModel

from package.routes.user.inputs.LoginInput import LoginInput
from tests.fixtures.register_user import RegisterResult
from tests.shared.ValidatingTokenResponse import ValidatingTokenResponse


class LoginResult(BaseModel):
    response: Response
    provided_data: LoginInput
    response_body: ValidatingTokenResponse

    class Config:
        arbitrary_types_allowed = True

    async def validate(self):
        await self.response_body.validate_user(self.provided_data)


PossibleAccessKey = Literal['email', 'username']
class LoginRequestor(Protocol):
    async def __call__(
        self,
        differing_field_key: PossibleAccessKey = 'email'
    ) -> LoginResult:
        ...


@pytest.fixture(scope='class')
def login_user(
    client: AsyncClient,
    register_user: RegisterResult
) -> LoginRequestor:
    async def _send_request(
        differing_field_key: PossibleAccessKey = 'email',
    ) -> LoginResult:
        register_data = register_user.provided_data
        data = LoginInput(
            usernameOrEmail=getattr(register_data, differing_field_key),
            password=register_data.password
        )

        response = await client.post('/login', json=data.dict())
        assert response.status_code == 200

        body = ValidatingTokenResponse[LoginInput].parse_obj(response.json())

        return LoginResult(
            provided_data=data,
            response=response,
            response_body=body
        )

    return _send_request
