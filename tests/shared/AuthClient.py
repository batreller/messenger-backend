from httpx import AsyncClient

from package.auth import get_current_user
from package.db.models.Chat import PublicChat
from package.db.models.Message import PublicMessageWithAuthor
from package.db.models.User import User
from package.routes.chat.endpoints.messages import MessagesPage
from package.routes.chat.inputs.CreateGroupInput import CreateGroupInput
from package.routes.chat.inputs.SendMessageInput import SendMessageInput


class AuthClient(AsyncClient):
    def __init__(self, *, token, faker, **kwargs):
        self.token = token
        self.faker = faker

        super().__init__(headers={
            'Authorization': f'Bearer {token}',
            **kwargs.get('headers', {})
        }, **kwargs)


    async def acquire_user(self) -> User:
        user = await get_current_user(self.token)

        return user


    async def send_message(self, chat_id: int) -> PublicMessageWithAuthor:
        data = SendMessageInput(
            contents=self.faker.text(1024)
        )

        response = await self.post(
            f'/chat/{chat_id}/message',
            json=data.dict()
        )

        assert response.status_code == 200
        assert response.json() is not None

        message = PublicMessageWithAuthor.construct(**response.json())
        return message


    async def create_group(self, with_ids: list[User] | int) -> PublicChat:
        if isinstance(with_ids, list):
            ids = [user.id for user in with_ids]
        else:
            ids = [with_ids]

        data = CreateGroupInput(
            with_ids=ids,
            name=self.faker.text(20)
        )

        response = await self.post(
            '/chat/group/create',
            json=data.dict()
        )

        assert response.status_code == 200
        assert response.json() is not None

        result = PublicChat.construct(**response.json())
        return result


    async def messages(self, chat_id: int) -> MessagesPage:
        result = await self.get(f'/chat/{chat_id}/messages')
        return MessagesPage.parse_obj(result.json())
