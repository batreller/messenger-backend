import typing

from tortoise import fields, signals
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


class Message(Model, BasePublicModel[PublicMessage], TimestampMixin):
    id = fields.IntField(pk=True, generated=False)
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
        # ! doesn't seem to work as a composite key. id is still the primary key in the db.
        unique_together = ('author_id', 'chat_id')


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


@signals.pre_save(Message)
async def signal_pre_save(
    sender: typing.Type[Message],
    instance: Message,
    *_
) -> None:
    prev_message = await sender.filter(
        author_id=instance.author_id,
        chat_id=instance.chat_id
    ).order_by('-id').first()

    if prev_message is None:
        instance.id = 0
        return

    instance.id = prev_message.id + 1
    print(dict(prev_message))
