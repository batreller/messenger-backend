import typing

from tortoise import fields
from tortoise.models import Model

from package.db.models.mixins.Timestamp import TimestampMixin

if typing.TYPE_CHECKING:
    from package.db.models.Chat import Chat
    from package.db.models.User import User


class Message(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    contents = fields.CharField(max_length=2047)

    chat: fields.ForeignKeyRelation['Chat'] = fields.ForeignKeyField(
        model_name='models.Chat',
        related_name='messages'
    )
    author: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        model_name='models.User'
    )
