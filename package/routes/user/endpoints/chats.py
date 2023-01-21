from datetime import datetime
from typing import Any

from fastapi import Depends, Query
from pydantic import BaseModel
from tortoise.transactions import in_transaction

from package.auth import auth_injector
from package.db.models.Chat import PublicChat
from package.db.models.User import User


class ChatsPage(BaseModel):
    count: int
    chats: list[PublicChat]


def parse_public_chat(data: dict[str, Any]) -> PublicChat:

    parse_message = data.get('message_id', None) is not None
    values: dict[str, Any] = {
        "last_message": {} if parse_message else None
    }

    for key, value in data.items():
        if key.startswith('message'):
            if not parse_message:
                continue

            values['last_message'][key.partition('_')[2]] = value
            continue

        values[key] = value

    return PublicChat.construct(**values)

# TODO: Add pagination
async def chats(
    user: User = Depends(auth_injector),
    time_cursor: datetime = Query(default=datetime.now(), alias='cursor'),
    limit: int = Query(default=25, lte=50)
) -> ChatsPage:
    async with in_transaction() as conn:
        # * Gets chats and last messages of those chats.
        # * The chats are ordered based on the time when the last message was sent.
        # * Done through are raw query, because the orm lacks functionality to select
        # * from fields on related tables.

        count, chats_data = await conn.execute_query('''
            select * from (
                select
                    distinct on (chat.id) chat.*,
                    message.id as message_id,
                    message.contents as message_contents,
                    message.created_at as message_created_at,
                    message.updated_at as message_updated_at,
                    message.author_id as message_author_id
                from chat
                left join message on chat.id=message.chat_id
                left join chat_participant on chat.id=chat_participant.chat_id
                where chat_participant.user_id=$1 and (
                    message.created_at < $2 or message.id is null
                )
                order by chat.id, message.created_at desc
                limit $3
            ) t
            order by t.message_created_at desc nulls last;
        ''', [user.id, time_cursor, limit])

    chats = []
    for chat in map(dict, chats_data):
        chats.append(parse_public_chat(chat))

    return ChatsPage(
        count=count,
        chats=chats
    )
