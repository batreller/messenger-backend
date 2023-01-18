from pydantic import BaseModel


class DeleteMessageInput(BaseModel):
    chat_id: int
    message_id: int
