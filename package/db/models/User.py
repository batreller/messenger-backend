from typing import Any

from tortoise import fields
from tortoise.models import Model

from package.db.models.mixins.Timestamp import TimestampMixin


class User(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=2048)
    email = fields.CharField(max_length=256, unique=True)

    def without_password(self) -> dict[str, Any]:
        as_dict = dict(self)
        del as_dict['password']

        return as_dict
