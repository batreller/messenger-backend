from fastapi import APIRouter

from package.routes.user.endpoints import bio, chats, me

router = APIRouter(prefix='/user')

router.add_api_route('/me', me.me, methods=['GET'])
router.add_api_route('/chats', chats.chats, methods=['GET'])
router.add_api_route('/bio', bio.bio, methods=['PATCH'])
