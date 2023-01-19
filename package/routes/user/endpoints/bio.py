import datetime

import tortoise.exceptions
from fastapi import APIRouter, Depends

from package.auth import auth_injector
from package.db.models.User import User
from package.routes.user.exceptions import invalid_bio
from package.routes.user.inputs.BioInput import BioInput

router = APIRouter()


@router.patch('/bio')
async def bio(data: BioInput, user: User = Depends(auth_injector)):
    try:
        await user.filter(id=user.id).update(about=data.bio, updated_at=datetime.datetime.now())
    except tortoise.exceptions.ValidationError:
        raise invalid_bio

    # TODO: maybe do it another way here
    user_instance = await user.filter(id=user.id).first()

    # FIXME
    return user_instance.without_password()
