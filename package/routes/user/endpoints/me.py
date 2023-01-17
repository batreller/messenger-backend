from fastapi import APIRouter
from fastapi import Depends

from package.auth import auth_injector
from package.db.models.User import User

router = APIRouter()


@router.get('/me')
async def me(user: User = Depends(auth_injector)):
    return user.without_password()
