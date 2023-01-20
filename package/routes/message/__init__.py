
from fastapi import APIRouter

from package.routes.message.endpoints import delete

router = APIRouter(prefix='/message/{message_id}')

router.add_api_route('', delete.delete, methods=['DELETE'])
