import pytest

from package.db.models.Message import Message, PublicMessageWithAuthor
from tests.shared.AuthClient import AuthClient


@pytest.mark.anyio
async def test_delete_message(
    auth_client: AuthClient,
    messages: list[PublicMessageWithAuthor]
):
    to_delete = messages.pop(len(messages) // 2)
    response = await auth_client.delete(
        f'/message/{to_delete.id}'
    )

    assert response.json()['success']
    deleted = await Message.filter(
        id=to_delete.id
    ).first()

    assert deleted is None
