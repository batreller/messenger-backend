from pydantic import BaseModel


class SendMessageInput(BaseModel):
    chat_id: int
    text: str
    # TODO: add images
