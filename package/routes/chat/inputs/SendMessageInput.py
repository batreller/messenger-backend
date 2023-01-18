from pydantic import BaseModel


class SendMessageInput(BaseModel):
    chat_id: int
    text: str
    # todo add images
