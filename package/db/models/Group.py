from tortoise import fields
from tortoise.models import Model

from package.db.models.mixins.Timestamp import TimestampMixin


class Group(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
