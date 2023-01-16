from tortoise import fields
from tortoise.models import Model

from package.db.models.Group import Group
from package.db.models.User import User
from package.db.models.mixins.Timestamp import TimestampMixin


class GroupMessage(Model, TimestampMixin):
    id = fields.IntField(pk=True)

    group: fields.ForeignKeyRelation[Group] = fields.ForeignKeyField(
        'models.Group'
    )
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User'
    )

    contents = fields.TextField()
