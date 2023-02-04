import typing

from tortoise import fields
from tortoise.models import Model
from tortoise.queryset import QuerySet

from package.db.BasePublicModel import BasePublicModel
from package.db.models.mixins.Timestamp import TimestampMixin
from package.db.models.User import ShortPublicUser
from package.db.PublicBase import PublicBase

if typing.TYPE_CHECKING:
    from package.db.models.Chat import Chat
    from package.db.models.User import User


class BasePublicMessage(PublicBase):
    contents: str

class PublicMessage(BasePublicMessage):
    author_id: int


class PublicMessageWithAuthor(BasePublicMessage):
    author: ShortPublicUser


# TODO: I think it's a good idea to setup a compond key for the chat_id and the id. The only problem is to setup the autoicrement to increment only when needed
class Message(Model, BasePublicModel[PublicMessage], TimestampMixin):
    id = fields.IntField(pk=True)
    contents = fields.CharField(max_length=2047)

    chat_id: int
    chat: fields.ForeignKeyRelation['Chat'] = fields.ForeignKeyField(
        model_name='models.Chat',
        related_name='messages'
    )

    author_id: int
    author: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        model_name='models.User'
    )


    class Meta:
        unique_together = ('id', 'chat_id')


    async def public(self) -> PublicMessage:
        data = dict(self)
        return PublicMessage.construct(**data)

    async def public_with_author(self) -> PublicMessageWithAuthor:
        if isinstance(self.author, QuerySet):
            await self.fetch_related('author')

        data = {
            **dict(self),
            "author": self.author
        }

        return PublicMessageWithAuthor.construct(**data)
