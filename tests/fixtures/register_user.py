import pytest
from faker import Faker
from httpx import AsyncClient, Response
from pydantic import BaseModel

from package.auth.get_current_user import get_current_user
from package.db.models.User import User
from package.routes.user.inputs.RegisterInput import RegisterInput
from tests.shared.ValidatingTokenResponse import ValidatingTokenResponse


class RegisterResult(BaseModel):
    response: Response
    response_body: ValidatingTokenResponse
    provided_data: RegisterInput

    class Config:
        arbitrary_types_allowed = True


    async def acquire_user(self) -> User:
        token = self.response_body.access_token
        user = await get_current_user(token)

        return user


async def register_call(
    faker: Faker,
    client: AsyncClient
) -> RegisterResult:
    data = RegisterInput(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password()
    )

    response = await client.post('/register', json=data.dict())

    return RegisterResult(
        response=response,
        response_body=ValidatingTokenResponse.parse_obj(response.json()),
        provided_data=data
    )


@pytest.fixture(scope='class')
async def register_user(
    faker: Faker,
    client: AsyncClient
) -> RegisterResult:
    result = await register_call(faker, client)
    return result


@pytest.fixture(scope='class')
async def other_register(
    faker: Faker,
    client: AsyncClient
) -> RegisterResult:
    other = await register_call(faker, client)
    return other
