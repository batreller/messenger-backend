import typing
from typing import Any

from tortoise import fields
from tortoise.models import Model

from package.db.models.mixins.Timestamp import TimestampMixin

if typing.TYPE_CHECKING:
    from package.db.models.Chat import Chat


class User(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=2047)
    email = fields.CharField(max_length=255, unique=True)
    email_confirmed = fields.BooleanField(default=False)
    bio = fields.CharField(max_length=64, null=True, default=None)

    chats: fields.ManyToManyRelation['Chat'] = fields.ManyToManyField(
        model_name='models.Chat',
        through='chat_participant',
        related_name='participants'
    )

    def without_password(self) -> dict[str, Any]:
        as_dict = dict(self)
        del as_dict['password']
        return as_dict
