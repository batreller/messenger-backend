from pydantic import BaseModel, validator

from package.db.models.User import User


class CreateInput(BaseModel):
    user_id: int

    @validator("user_id", pre=True)
    def user_exists(cls, value):
        user = User.get(id=value)
        if user:
            return value
        else:
            raise ValueError("User not exists")
