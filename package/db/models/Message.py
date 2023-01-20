import typing

from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model
from tortoise.queryset import QuerySet

from package.db.BasePublicModel import BasePublicModel
from package.db.models.mixins.Timestamp import TimestampMixin
from package.db.PublicBase import PublicBase

if typing.TYPE_CHECKING:
    from package.db.models.Chat import Chat
    from package.db.models.User import User


class PublicAuthor(BaseModel):
    id: int
    username: str


class PublicMessage(PublicBase):
    contents: str
    author: PublicAuthor


# TODO: I think it's a good idea to setup a compond key for the chat_id and the id. The only problem is to setup the autoicrement to increment only when needed
class Message(Model, BasePublicModel[PublicMessage], TimestampMixin):
    id = fields.IntField(pk=True)
    contents = fields.CharField(max_length=2047)

    chat: fields.ForeignKeyRelation['Chat'] = fields.ForeignKeyField(
        model_name='models.Chat',
        related_name='messages'
    )
    author: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        model_name='models.User'
    )


    async def public(self) -> PublicMessage:
        if isinstance(self.author, QuerySet):
            await self.fetch_related('author')

        return PublicMessage.parse_obj({
            **dict(self),
            "author": self.author
        })
