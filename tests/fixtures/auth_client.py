from typing import AsyncIterable

import pytest
from httpx import AsyncClient

from package.__main__ import app
from package.auth.get_current_user import get_current_user
from package.db.models.User import User
from tests.fixtures.login_user import LoginRequestor


class AuthClient(AsyncClient):
    def __init__(self, *, token, **kwargs):
        self.token = token

        super().__init__(headers={
            'Authorization': f'Bearer {token}',
            **kwargs.get('headers', {})
        }, **kwargs)


    async def acquire_user(self) -> User:
        user = await get_current_user(self.token)

        return user


@pytest.fixture(scope='class')
async def auth_client(
    login_user: LoginRequestor
) -> AsyncIterable[AsyncClient]:
    login_result = await login_user()
    token = login_result.response_body.access_token

    async with AuthClient(
        token=token,
        app=app,
        base_url="http://test"
    ) as auth_client:
        yield auth_client
