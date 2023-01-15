from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from package.config import config


def register_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=config.db.connection_string,
        modules={
            "models": [
                "package.db.models.User",
                "package.db.models.Chat",
                "package.db.models.ChatParticipant"
            ]
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )
