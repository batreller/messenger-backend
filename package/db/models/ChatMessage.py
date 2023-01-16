from tortoise import fields
from tortoise.models import Model

from package.db.models.Chat import Chat
from package.db.models.User import User
from package.db.models.mixins.Timestamp import TimestampMixin


class ChatMessage(Model, TimestampMixin):
    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        'models.Chat'
    )
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User'
    )

    contents = fields.TextField()
