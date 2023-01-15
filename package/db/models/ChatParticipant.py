from tortoise import fields
from tortoise.models import Model

from package.db.models.Chat import Chat
from package.db.models.User import User


class ChatParticipant(Model):
    chat_id: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        'models.Chat'
    )
    user_id: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User'
    )

    joined_at = fields.DatetimeField(auto_now_add=True)
