from fastapi import APIRouter

from package.routes.chat.endpoints import create
from package.routes.chat.endpoints import send_message
from package.routes.chat.endpoints import delete_message
from package.routes.chat.endpoints import messages

router = APIRouter(prefix='/chat')

router.include_router(create.router)
router.include_router(send_message.router)
router.include_router(delete_message.router)
router.include_router(messages.router)
