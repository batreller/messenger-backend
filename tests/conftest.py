from urllib.parse import urlparse

import asyncpg
import pytest
from faker import Faker
from httpx import AsyncClient
from tortoise import Tortoise

from package.__main__ import app
from package.db import TORTOISE_ORM

pytest_plugins = [
    'tests.fixtures.register_user',
    'tests.fixtures.login_user',
    'tests.fixtures.auth_client',
    'tests.test_message.fixtures.chat',
    'tests.test_message.fixtures.messages'
]

async def create_db(db_url: str):
    data = urlparse(db_url)
    db = data.path.partition('/')[2]
    owner = data.netloc.partition('@')[0].partition(':')[0]

    try:
        conn = await asyncpg.connect(db_url)
        await conn.execute(
            f'DROP DATABASE "{db}"'
        )

        await conn.close()
    except asyncpg.InvalidCatalogNameError:
        print(f'{db} database already exists!')

    conn = await asyncpg.connect(
        db_url,
        database='template1'
    )

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


async def init():
    await init_db()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope='session')
async def faker():
    faker = Faker()
    yield faker


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()
