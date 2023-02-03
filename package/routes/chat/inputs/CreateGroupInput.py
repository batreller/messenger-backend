from pydantic import BaseModel, Field


class CreateGroupInput(BaseModel):
    with_ids: list[int] = Field(min_items=1)
    name: str = Field(max_length=255)
