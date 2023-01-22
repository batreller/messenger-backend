from fastapi import APIRouter, Depends, Header

from package.auth import TokenResponse
from package.routes.auth.endpoints import login, register
from package.routes.auth.exceptions import already_authenticated


async def not_auth(auth_header = Header(alias='Authorization', default=None)):
    if auth_header is not None:
        raise already_authenticated


router = APIRouter(
    dependencies=[
        Depends(not_auth)
    ]
)

router.add_api_route(
    '/login',
    login.login,
    methods=['POST'],
    response_model=TokenResponse
)

router.add_api_route(
    '/register',
    register.register,
    methods=['POST'],
    response_model=TokenResponse
)
