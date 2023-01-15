from tortoise import fields
from tortoise.models import Model


class Chat(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now=True)
