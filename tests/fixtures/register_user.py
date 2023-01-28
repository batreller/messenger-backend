import pytest
from faker import Faker
from httpx import AsyncClient, Response
from pydantic import BaseModel

from package.routes.user.inputs.RegisterInput import RegisterInput
from tests.shared.ValidatingTokenResponse import ValidatingTokenResponse


class RegisteredUser(BaseModel):
    response: Response
    response_body: ValidatingTokenResponse
    provided_data: RegisterInput

    class Config:
        arbitrary_types_allowed = True


@pytest.fixture(scope='module')
async def register_user(
    faker: Faker,
    client: AsyncClient
):
    data = {
        "username": faker.user_name(),
        "email": faker.email(),
        "password": faker.password()
    }

    to_assert_data = data.copy()
    del to_assert_data['password']

    response = await client.post('/register', json=data)

    yield RegisteredUser(
        response=response,
        response_body=ValidatingTokenResponse.parse_obj(response.json()),
        provided_data=RegisterInput.parse_obj(data)
    )
