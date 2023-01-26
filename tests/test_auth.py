from unittest import TestCase

import pytest
from faker import Faker
from faker.providers import internet
from httpx import AsyncClient

from package.auth import TokenResponse, get_current_user

fake = Faker()
fake.add_provider(internet.Provider)


@pytest.mark.anyio
async def test_register(client: AsyncClient):
    data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password()
    }

    to_assert_data = data.copy()
    del to_assert_data['password']

    response = await client.post('/register', json=data)
    body = TokenResponse.validate(response.json()) 

    assert body.token_type.lower() == 'bearer'

    authenticated_user = await get_current_user(body.access_token)
    needed_data = {key: getattr(authenticated_user, key) for key in to_assert_data.keys()}
    TestCase().assertDictEqual(to_assert_data, needed_data)

    assert response.status_code == 200
