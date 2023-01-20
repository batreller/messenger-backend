from pydantic import BaseModel


class SendMessageInput(BaseModel):
    contents: str
    # TODO: add images
