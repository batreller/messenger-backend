from tortoise import fields
from tortoise.models import Model

from package.db.models.User import User
from package.db.models.mixins.Timestamp import TimestampMixin


class Chat(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    first_user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        related_name='first_user'
    )
    second_user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        related_name='second_user'
    )
