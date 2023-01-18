from pydantic import BaseModel


class MessagesInput(BaseModel):
    chat_id: int
