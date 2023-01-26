from urllib.parse import urlparse

import asyncpg
import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from package.__main__ import app
from package.db import TORTOISE_ORM


async def create_db(db_url: str):
    conn = await asyncpg.connect(
        db_url,
        database='template1'
    )

    data = urlparse(db_url)
    db = data.path.partition('/')[2]
    owner = data.netloc.partition('@')[0].partition(':')[0]

    await conn.execute(
        f'CREATE DATABASE "{db}" OWNER "{owner}"'
    )


async def init_db(
    db_url = TORTOISE_ORM['connections']['default'],
    schemas: bool = True
) -> None:
    await create_db(db_url)
    await Tortoise.init(
        config=TORTOISE_ORM
    )

    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init():
    await init_db()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()
