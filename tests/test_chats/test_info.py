import pytest

from package.db.models.Chat import PublicChat, PublicChatWithParticipants
from package.db.models.User import User
from tests.shared.assert_ids import assert_ids
from tests.shared.AuthClient import AuthClient
from tests.shared.TestIntersections import TestIntersections


@pytest.mark.anyio
async def test_info(
    auth_client: AuthClient,
    chat: PublicChat
):
    response = await auth_client.get(f'/chat/{chat.id}')
    pure_body = response.json()
    body = PublicChatWithParticipants.parse_obj(pure_body)
    db_participants = await User.filter(
        id__in=[user.id for user in body.participants]
    )

    assert_ids(db_participants, body.participants)
    TestIntersections(set(['participants'])).assert_dicts(pure_body, chat.dict())
