import urllib.parse
from typing import Any, AsyncIterable

import pytest
from faker import Faker
from httpx import AsyncClient

from package.db.models.Chat import Chat, PublicChat
from package.db.models.Message import PublicMessage
from package.routes.chat.inputs.CreateGroupInput import CreateGroupInput
from package.routes.chat.inputs.SendMessageInput import SendMessageInput
from tests.fixtures.auth_client import AuthClient
from tests.fixtures.register_user import RegisterResult

FAKE_CHATS_COUNT = 10

ChatResponse = dict[str, Any]


@pytest.fixture()
async def chats(
    auth_client: AsyncClient,
    other_register: RegisterResult,
    faker: Faker,
) -> AsyncIterable[list[PublicChat]]:
    other_user = await other_register.acquire_user()
    body = CreateGroupInput(
        with_ids=[other_user.id],
        name=''
    )

    chats: list[PublicChat] = []
    for _ in range(FAKE_CHATS_COUNT):
        body.name = faker.text(20)
        response = await auth_client.post(
            '/chat/group/create',
            json=body.dict()
        )

        assert response.status_code == 200
        chats.append(PublicChat.construct(**response.json()))

    chats.reverse()
    yield chats

    ids = [chat.id for chat in chats]
    affected = await Chat.filter(
        id__in=ids
    ).delete()

    assert affected == len(ids)


def access_id(with_id) -> int:
    if isinstance(with_id, dict):
        return with_id['id']
    else:
        return with_id.id

def assert_ids(first: list[PublicChat], second: list[PublicChat]) -> None:
    first_ids = [access_id(item) for item in first]
    second_ids = [access_id(item) for item in second]

    assert first_ids == second_ids


class TestChats:
    @pytest.mark.anyio
    async def test_no_messages(
        self,
        auth_client: AuthClient,
        chats: list[PublicChat]
    ):
        response = await auth_client.get('/user/chats')
        retrieved_chats = response.json()['chats']

        assert_ids(chats, retrieved_chats)


    @pytest.mark.anyio
    async def test_with_messages(
        self,
        chats: list[PublicChat],
        faker: Faker,
        auth_client: AuthClient
    ):
        half = len(chats) // 2
        first_part, last_part = chats[:half], chats[half:]

        last_messages = []
        for chat in last_part:
            response = None
            for _ in range(5):
                body = SendMessageInput(
                    contents=faker.text(1024)
                )

                response = await auth_client.post(
                    f'/chat/{chat.id}/message',
                    json=body.dict()
                )

            if response is None:
                continue

            last_messages.append(PublicMessage.construct(**response.json()))


        response = await auth_client.get('/user/chats')
        retrieved_chats = response.json()['chats']

        assert_ids([*reversed(last_part), *first_part], retrieved_chats)


    @pytest.mark.anyio
    async def test_pagination(
        self,
        chats: list[PublicChat],
        auth_client: AuthClient
    ):
        half = FAKE_CHATS_COUNT // 2

        first_response = await auth_client.get(f'/user/chats?limit={half}')
        first_json = first_response.json()
        first_part = first_json['chats']

        assert first_json['next'] is not None
        cursor_string = urllib.parse.quote(first_json['next'])

        second_part = await auth_client.get(
            f'/user/chats?cursor={cursor_string}'
        )

        second_part = second_part.json()['chats']

        assert_ids(chats, [*first_part, *second_part])
