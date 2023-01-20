from pydantic import BaseModel, Field


class CreateGroupInput(BaseModel):
    with_ids: list[str] = Field(min_items=1)
    name: str
