from pydantic import BaseModel


class CreatePrivateInput(BaseModel):
    with_user_id: int
