import pytest

from tests.fixtures.login_user import LoginRequestor


class TestLogin:
    @pytest.mark.anyio
    async def test_email_login(
        self,
        login_user: LoginRequestor
    ):
        response = await login_user('email')
        await response.validate()


    @pytest.mark.anyio
    async def test_username_login(
        self,
        login_user: LoginRequestor
    ):
        response = await login_user('username')
        await response.validate()
