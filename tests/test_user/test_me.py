import pytest

from package.auth import get_current_user
from tests.fixtures.auth_client import AuthClient
from tests.shared.TestIntersections import TestIntersections


@pytest.mark.anyio
async def test_me(auth_client: AuthClient):
    response = await auth_client.get('/user/me')
    body = response.json()

    this_user = await get_current_user(auth_client.token)
    TestIntersections().assert_dicts(body, dict(this_user))
