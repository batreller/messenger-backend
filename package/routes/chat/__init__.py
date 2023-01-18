from fastapi import APIRouter

from package.routes.chat.endpoints import create

router = APIRouter(prefix='/chat')

router.include_router(create.router)
