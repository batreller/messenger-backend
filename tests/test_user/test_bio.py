import pytest
from faker import Faker

from package.routes.user.inputs.BioInput import BioInput
from tests.fixtures.auth_client import AuthClient


@pytest.mark.anyio
async def test_bio(
    auth_client: AuthClient,
    faker: Faker
):
    before = await auth_client.acquire_user()

    assert before.bio is None

    body = BioInput(
        bio=faker.sentence()
    )

    response = await auth_client.patch('/user/bio', json=body.dict())
    after = await auth_client.acquire_user()

    assert response.json()['success']
    assert after.bio == body.bio
