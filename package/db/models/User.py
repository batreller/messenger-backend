from typing import Any

from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=1024, unique=True)
    password = fields.CharField(max_length=2048)
    email = fields.CharField(max_length=256, unique=True)

    # TODO: Use a mixin
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def without_password(self) -> dict[str, Any]:
        as_dict = dict(self)
        del as_dict['password']

        return as_dict
