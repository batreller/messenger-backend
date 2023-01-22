import typing

from tortoise import fields
from tortoise.models import Model

if typing.TYPE_CHECKING:
    from package.db.models.Chat import Chat
    from package.db.models.User import User


class ChatParticipant(Model):
    chat: fields.ForeignKeyRelation['Chat'] = fields.ForeignKeyField(
        'models.Chat',
        'chat_participants'
    )
    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User',
        'chat_participants'
    )

    joined_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'chat_participant'

