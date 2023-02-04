import random

import pytest

from package.db.models.Chat import PublicChat
from package.db.models.Message import PublicMessageWithAuthor
from package.db.models.User import User
from package.routes.chat.endpoints.messages import MessagesPage
from tests.fixtures.auth_client import AuthClient
from tests.shared.assert_ids import assert_ids


class TestMessages():
    @pytest.mark.anyio
    async def test_simple(
        self,
        auth_client: AuthClient,
        chat: PublicChat,
        messages: list[PublicMessageWithAuthor]
    ):
        response = await auth_client.get(
            f'/chat/{chat.id}/messages'
        )

        assert response.status_code == 200
        body = MessagesPage.parse_obj(response.json())

        assert body.count == len(messages)

        author_ids = [author.id for author in body.authors]
        db_authors = await User.filter(
            id__in=author_ids
        )

        author_ids_from_objects = []
        for message in body.messages:
            if message.author_id in author_ids_from_objects:
                continue

            author_ids_from_objects.append(message.author_id)

        assert author_ids_from_objects == author_ids
        assert_ids(db_authors, body.authors)
        assert_ids(body.messages, messages)


    @pytest.mark.anyio
    async def test_pagination(
        self,
        auth_client: AuthClient,
        chat: PublicChat,
        messages: list[PublicMessageWithAuthor]
    ):
        half = len(messages) // 2
        first_half = await auth_client.get(
            f'/chat/{chat.id}/messages?limit={half}'
        )

        first_messages = first_half.json()['messages']
        last_id = first_messages[-1]['id']

        assert len(first_messages) == half
        assert last_id == messages[half - 1].id

        second_half = await auth_client.get(
            f'/chat/{chat.id}/messages?cursor={last_id}'
        )

        second_messages = second_half.json()['messages']

        assert_ids(messages, [*first_messages, *second_messages])


    @pytest.mark.anyio
    async def test_deleting_messages(
        self,
        auth_client: AuthClient,
        messages: list[PublicMessageWithAuthor],
        chat: PublicChat
    ):
        before_response = await auth_client.messages(chat.id)
        random_messages = random.choices(messages, k=len(messages) // 4)
        ids = set([message.id for message in random_messages])

        for _id in ids:
            response = await auth_client.delete(f'/message/{_id}')
            assert response.json()['success']

        after_response = await auth_client.messages(chat.id)
        cleared = filter(
            lambda message: message.id not in ids,
            before_response.messages
        )

        assert_ids(cleared, after_response.messages)
