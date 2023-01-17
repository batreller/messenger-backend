from pydantic import BaseModel


class BioInput(BaseModel):
    bio: str
