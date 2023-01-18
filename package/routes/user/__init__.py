from fastapi import APIRouter

from package.routes.user.endpoints import login
from package.routes.user.endpoints import me
from package.routes.user.endpoints import register
from package.routes.user.endpoints import bio
from package.routes.user.endpoints import chats
from package.routes.user.exceptions import user_exists
from package.routes.user.exceptions import user_exists, wrong_credentials
from package.routes.user.hasher import ph
from package.routes.user.inputs.LoginInput import LoginInput
from package.routes.user.inputs.RegisterInput import RegisterInput
from package.routes.user.inputs.RegisterInput import RegisterInput

router = APIRouter(prefix='/user')

router.include_router(register.router)
router.include_router(login.router)
router.include_router(me.router)
router.include_router(bio.router)
router.include_router(chats.router)
