import asyncio
from typing import Any, Coroutine

from fastapi import Depends, Query
from pydantic import BaseModel

from package.db.models.Chat import Chat
from package.db.models.Message import PublicAuthor, PublicMessage
from package.routes.chat.dependencies.chat_participant_of import chat_participant_of


class MessagesPage(BaseModel):
    count: int
    authors: list[PublicAuthor]
    messages: list[PublicMessage]


async def messages(
    chat: Chat = Depends(chat_participant_of),
    limit: int = Query(default=50, lte=100),
    id_cursor: int | None = Query(default=None, alias='cursor')
) -> MessagesPage:
    messages_query = chat.messages \
        .order_by('created_at') \
        .limit(limit)

    if id_cursor is not None:
        messages_query = chat.messages.filter(
            id__gt=id_cursor
        )


    author_ids = set()
    tasks: list[Coroutine[Any, Any, PublicMessage]] = []
    async for message in messages_query:
        author_ids.add(message.author_id)
        tasks.append(message.public())

    messages = await asyncio.gather(*tasks)
    authors = list(map(
        lambda user: user.author(),
        await chat.participants.filter(
            id__in=author_ids
        )
    ))


    return MessagesPage(
        count=len(messages),
        authors=authors,
        messages=messages,
    )
