import argon2
from tortoise.expressions import Q

from package.auth import TokenResponse
from package.auth.create_access_token import create_access_token
from package.db.models.User import User
from package.routes.auth.exceptions import wrong_credentials
from package.routes.user.hasher import ph
from package.routes.user.inputs.LoginInput import LoginInput


async def login(data: LoginInput) -> TokenResponse:
    predicate = await User.filter(
        Q(username=data.usernameOrEmail) | Q(email=data.usernameOrEmail)
    ).first()

    if predicate is None:
        raise wrong_credentials

    try:
        ph.verify(predicate.password, data.password)
    except argon2.exceptions.VerifyMismatchError:
        raise wrong_credentials

    token = create_access_token({
        "user_id": predicate.id
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )
