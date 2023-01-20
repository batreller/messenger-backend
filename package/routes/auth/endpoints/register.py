from tortoise.expressions import Q

from package.auth import TokenResponse
from package.auth.create_access_token import create_access_token
from package.db.models.User import User
from package.routes.auth.exceptions import user_exists
from package.routes.user.hasher import ph
from package.routes.user.inputs.RegisterInput import RegisterInput


async def register(data: RegisterInput) -> TokenResponse:
    predicate = await User.filter(
        Q(username=data.username) | Q(email=data.email)
    ).first()

    if predicate is not None:
        raise user_exists

    new_user = await User.create(
        password=ph.hash(data.password),
        username=data.username,
        email=data.email
    )

    await new_user.save()
    token = create_access_token({
        "user_id": new_user.id
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )
