from typing import Any

from tortoise import fields
from tortoise.models import Model

from package.db.models.mixins.Timestamp import TimestampMixin


class User(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=2047)
    email = fields.CharField(max_length=255, unique=True)
    email_confirmed = fields.BooleanField(default=False)
    about = fields.CharField(max_length=64, null=True, default=None)

    def without_password(self) -> dict[str, Any]:
        as_dict = dict(self.__dict__)
        as_dict.pop('password', as_dict)
        return as_dict
