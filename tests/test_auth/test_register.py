import pytest

from tests.fixtures.register_user import RegisterResult


@pytest.mark.anyio
async def test_register(register_user: RegisterResult):
    to_assert_data = register_user.provided_data.dict().copy()
    del to_assert_data['password']

    assert register_user.response_body.token_type.lower() == 'bearer'
    assert register_user.response.status_code == 200
    await register_user.response_body.validate_user(register_user.provided_data)
