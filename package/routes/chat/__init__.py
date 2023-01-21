from fastapi import APIRouter

from package.routes.chat.endpoints import (
    create_group,
    create_private,
    message,
    messages,
)

router = APIRouter(prefix='/chat')

router.add_api_route('/private/create', create_private.create_private, methods=['POST'])
router.add_api_route('/group/create', create_group.create_group, methods=['POST'])
router.add_api_route('/{chat_id}/message', message.send_message, methods=['POST'])
router.add_api_route(
    '/{chat_id}/messages', 
    messages.messages,
    methods=['GET'],
    response_model=messages.MessagesPage
)
