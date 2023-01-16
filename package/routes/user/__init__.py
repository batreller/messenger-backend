import argon2
from argon2 import PasswordHasher
from fastapi import APIRouter, Depends
from tortoise.expressions import Q

from package.auth import TokenResponse, auth_injector
from package.auth.create_access_token import create_access_token
from package.db.models.User import User
from package.routes.user.exceptions import user_exists, wrong_credentials
from package.routes.user.inputs.LoginInput import LoginInput
from package.routes.user.inputs.RegisterInput import RegisterInput

router = APIRouter(prefix='/user')
ph = PasswordHasher()


@router.post('/register', response_model=TokenResponse)
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


@router.post('/login', response_model=TokenResponse)
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


@router.get('/me')
async def me(user: User = Depends(auth_injector)):
    return user.without_password()
