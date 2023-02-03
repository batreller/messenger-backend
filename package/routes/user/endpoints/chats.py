import json
from datetime import datetime

from fastapi import Depends, Query
from pydantic import BaseModel
from tortoise.transactions import in_transaction

from package.auth import auth_injector
from package.db.models.Chat import PublicChat
from package.db.models.User import User


class ChatsPage(BaseModel):
    next: datetime | None
    count: int
    chats: list[PublicChat]


async def chats(
    user: User = Depends(auth_injector),
    time_cursor: datetime | None = Query(default=None, alias='cursor'),
    limit: int = Query(default=25, lte=50)
) -> ChatsPage:
    if time_cursor is None:
        time_cursor = datetime.now()

    async with in_transaction() as conn:
        # * Gets chats and last messages of those chats.
        # * The chats are ordered based on the time when the last message was sent.
        # * Done through are raw query, because the orm lacks functionality to select
        # * from fields on related tables.

        count, chats_data = await conn.execute_query('''
            select * from (
                select
                    distinct on (chat.id) chat.*,
                    to_json(message) as last_message,
                    coalesce(message.created_at, chat.updated_at) as last_interacted
                from chat
                left join message on message.chat_id = chat.id
                join chat_participant cp on cp.chat_id = chat.id and cp.user_id = $1
                where coalesce(message.created_at, chat.updated_at) < $2
            ) as nested
            order by nested.last_interacted desc
            limit $3;
        ''', [user.id, time_cursor, limit])

    chats = []
    for chat in map(dict, chats_data):
        if chat['last_message'] is not None:
            chat['last_message'] = json.loads(chat['last_message'])

        chats.append(PublicChat.construct(**chat))

    next_cursor = None
    if len(chats) > 0:
        next_cursor = dict(chats_data[-1]).get('last_interacted', None)

    return ChatsPage(
        next=next_cursor,
        count=count,
        chats=chats,
    )
