from fastapi import APIRouter

from package.routes.user.endpoints import login
from package.routes.user.endpoints import me
from package.routes.user.endpoints import register
from package.routes.user.endpoints import bio
from package.routes.user.endpoints import chats

router = APIRouter(prefix='/user')

router.include_router(register.router)
router.include_router(login.router)
router.include_router(me.router)
router.include_router(bio.router)
router.include_router(chats.router)
