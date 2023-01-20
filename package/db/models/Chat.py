import typing
from enum import Enum

from tortoise import fields
from tortoise.models import Model

from package.db.models.mixins.Timestamp import TimestampMixin

if typing.TYPE_CHECKING:
    from package.db.models.Message import Message
    from package.db.models.User import User


class ChatType(str, Enum):
    private = 'private'
    group = 'group'


class Chat(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True, required=False)
    type = fields.CharEnumField(ChatType)
    creator = fields.ForeignKeyField(
        'models.User',
        'created_by_chats'
    )

    participants: fields.ManyToManyRelation['User']
    messages: fields.ReverseRelation['Message']

