from fastapi import Depends

from package.auth import auth_injector
from package.db.models.User import User
from package.routes.user.inputs.BioInput import BioInput
from package.shared.SuccessResponse import SuccessResponse


async def bio(
    data: BioInput,
    user: User = Depends(auth_injector)
) -> SuccessResponse:
    user.update_from_dict(data.dict())

    return SuccessResponse()