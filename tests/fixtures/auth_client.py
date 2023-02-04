from typing import AsyncIterable

import pytest
from faker import Faker
from httpx import AsyncClient

from package.__main__ import app
from tests.fixtures.login_user import LoginRequestor
from tests.shared.AuthClient import AuthClient


@pytest.fixture(scope='class')
async def auth_client(
    login_user: LoginRequestor,
    faker: Faker
) -> AsyncIterable[AsyncClient]:
    login_result = await login_user()
    token = login_result.response_body.access_token

    async with AuthClient(
        token=token,
        faker=faker,
        app=app,
        base_url="http://test"
    ) as auth_client:
        yield auth_client
