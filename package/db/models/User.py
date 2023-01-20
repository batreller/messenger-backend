from __future__ import annotations

import typing

from tortoise import fields
from tortoise.models import Model

from package.db.BasePublicModel import BasePublicModel
from package.db.models.mixins.Timestamp import TimestampMixin
from package.db.PublicBase import PublicBase

if typing.TYPE_CHECKING:
    from package.db.models.Chat import Chat


class PublicUser(PublicBase):
    username: str
    email: str
    bio: str | None
    email_confirmed: bool


class User(Model, BasePublicModel[PublicUser], TimestampMixin):
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

    def public(self) -> PublicUser:
        as_dict = dict(self)
        return PublicUser.parse_obj(as_dict)
