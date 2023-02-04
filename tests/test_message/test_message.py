import pytest

from package.db.models.Chat import PublicChat
from package.db.models.Message import Message
from tests.fixtures.auth_client import AuthClient
from tests.shared.TestIntersections import TestIntersections


class TestMessage():
    @pytest.mark.anyio
    async def test_message(
        self,
        auth_client: AuthClient,
        chat: PublicChat
    ):
        message = await auth_client.send_message(chat.id)
        db_message = await Message.filter(id=message.id).first()

        assert db_message is not None

        TestIntersections().assert_dicts(dict(db_message), message)
