
from typing import AsyncIterable

import pytest

from package.db.models.Chat import PublicChat
from package.db.models.Message import Message, PublicMessageWithAuthor
from tests.shared.AuthClient import AuthClient

NUMBER_OF_MESSAGES = 20


@pytest.fixture()
async def messages(
    auth_client: AuthClient,
    chat: PublicChat
) -> AsyncIterable[list[PublicMessageWithAuthor]]:
    messages = []
    ids = []
    for _ in range(NUMBER_OF_MESSAGES):
        message = await auth_client.send_message(chat.id)
        ids.append(message.id)
        messages.append(message)

    yield messages

    affected = await Message.filter(
        id__in=ids
    ).delete()

    assert affected > 0
