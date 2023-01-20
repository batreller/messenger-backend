import tortoise.exceptions
from fastapi import Depends

from package.auth import auth_injector
from package.db.models.User import User
from package.routes.user.exceptions import invalid_bio
from package.routes.user.inputs.BioInput import BioInput


async def bio(data: BioInput, user: User = Depends(auth_injector)):
    try:
        user.update_from_dict(data.dict())

    # FIXME: Should be removed when proper validation with pydantic will be added
    except tortoise.exceptions.ValidationError:
        raise invalid_bio

    # TODO: Proper type.
    return {
        "success": True
    }
