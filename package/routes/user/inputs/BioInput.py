from pydantic import BaseModel, Field


class BioInput(BaseModel):
    bio: str = Field(max_length=64)
