from pydantic import BaseModel, Field


class SendMessageInput(BaseModel):
    contents: str = Field(max_length=2047)
    # TODO: add images
