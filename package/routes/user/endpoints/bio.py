from fastapi import Depends

from package.auth import auth_id
from package.db.models.User import User
from package.routes.user.inputs.BioInput import BioInput
from package.shared.SuccessResponse import SuccessResponse


async def bio(
    data: BioInput,
    user_id: int = Depends(auth_id)
) -> SuccessResponse:
    updated_count = await User.filter(id=user_id).update(**data.dict())

    return SuccessResponse(
        success=updated_count >= 1
    )
