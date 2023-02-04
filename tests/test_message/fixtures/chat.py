from typing import AsyncIterable
import pytest
from package.db.models.Chat import Chat, PublicChat
from tests.fixtures.register_user import RegisterResult

from tests.shared.AuthClient import AuthClient


@pytest.fixture()
async def chat(
    auth_client: AuthClient,
    other_register: RegisterResult
) -> AsyncIterable[PublicChat]:
    other_user = await other_register.acquire_user()
    chat = await auth_client.create_group(other_user.id)
    yield chat

    affected = await Chat.filter(
        id=chat.id
    ).delete()

    assert affected >= 1
