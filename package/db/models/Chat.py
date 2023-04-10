import typing
from enum import Enum

from tortoise import fields
from tortoise.models import Model

from package.db.BasePublicModel import BasePublicModel
from package.db.models.Message import PublicMessage
from package.db.models.mixins.Timestamp import TimestampMixin
from package.db.models.User import ShortPublicUser
from package.db.PublicBase import PublicBase

if typing.TYPE_CHECKING:
    from package.db.models.Message import Message
    from package.db.models.User import User


class ChatType(str, Enum):
    private = 'private'
    group = 'group'


class PublicChat(PublicBase):
    name: str | None
    type: ChatType
    last_message: PublicMessage | None


class PublicChatWithParticipants(PublicChat):
    participants: list[ShortPublicUser]


class Chat(Model, BasePublicModel[PublicChat], TimestampMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True, required=False)
    type = fields.CharEnumField(ChatType)
    creator = fields.ForeignKeyField(
        'models.User',
        'created_by_chats'
    )

    participants: fields.ManyToManyRelation['User']
    messages: fields.ReverseRelation['Message']


    async def public(self) -> PublicChat:
        last_message = await self.messages.order_by('created_at').first()
        if last_message is not None:
            last_message = await last_message.public()

        return PublicChat.parse_obj({
            "last_message": last_message,
            **dict(self)
        })

    async def public_with_participants(self) -> PublicChatWithParticipants:
        simple_public = await self.public()

        participants_data = await self.participants.all()
        participants = []

        for item in participants_data:
            participants.append(item.public())

        result = PublicChatWithParticipants.construct(
            **dict(simple_public),
            participants=participants
        )

        return result
